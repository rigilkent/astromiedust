import pickle
import h5py
import numpy as np

__all__ = ["SystemResult", "OpticalModel"]

class SystemResult:
    """Container for saving, loading, and exporting computation results.
    
    This class serves as a container to serialize/deserialize computation results.
    After loading, it provides direct access to both the star configuration
    and all particle properties, including their material properties (prtl.matrl).

    Attributes:
        star (Star): Input star object
        prtl (Particles): Particles object containing all computed properties, 
                         including material properties via prtl.matrl
    """
    def __init__(self, star=None, prtl=None):
        if star is None and prtl is None:
            raise ValueError("At least one of star or prtl must be provided.")

        self.star = star
        self.prtl = prtl
    
    def save(self, file_name):
        """Save the complete result to a file using pickle."""
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)
        
    def save_hdf5(self, file_name):
        """
        Save the complete result to an HDF5 file for interoperability.
        
        Args:
            file_name (str): Path to the HDF5 file to create.
        """
        with h5py.File(file_name, 'w') as f:
            def _save_attr(group, name, value):
                """Helper to save HDF5 attributes with type conversion for path objects."""
                if value is None:
                    return
                # Convert Path objects or other non-standard types to strings
                if not isinstance(value, (int, float, bool, str, np.number, np.bool_)):
                    value = str(value)
                group.attrs[name] = value

            if self.star:
                star_grp = f.create_group('star')
                # Save attributes (scalars/strings)
                for attr in ['name', 'temp', 'lum_suns', 'mass_suns', 'is_blackbody', 'spectrum_file']:
                    if hasattr(self.star, attr):
                        _save_attr(star_grp, attr, getattr(self.star, attr))
                
                # Save datasets (arrays)
                for attr in ['wavs', 'flux_lam', 'flux_nu', 'log_wavs', 'log_flux_lam', 'log_flux_nu']:
                    if hasattr(self.star, attr):
                        val = getattr(self.star, attr)
                        if val is not None:
                            star_grp.create_dataset(attr, data=val)
            
            if self.prtl:
                prtl_grp = f.create_group('particles')
                # Save attributes
                for attr in ['suppress_mie_resonance', 'size_averaging_window', 'precompute_Qs']:
                    if hasattr(self.prtl, attr):
                        _save_attr(prtl_grp, attr, getattr(self.prtl, attr))
                
                # Save datasets
                for attr in ['diams', 'wavs', 'dists', 'temps', 'Qabs', 'Qpr', 'Qsca', 'Qpr_star_avg', 'betas', 'bnus', 'diams_blow']:
                    if hasattr(self.prtl, attr):
                        val = getattr(self.prtl, attr)
                        if val is not None:
                            # Handle tuples like diams_blow
                            if isinstance(val, tuple):
                                val = np.array(val)
                            prtl_grp.create_dataset(attr, data=val)
                
                if hasattr(self.prtl, 'matrl') and self.prtl.matrl:
                    mat_grp = prtl_grp.create_group('material')
                    mat = self.prtl.matrl
                    # Save attributes
                    attrs = ['qsil', 'qice', 'mpor', 'cryst', 'emt', 'refmed', 'qsil_tot', 'qorg_tot', 'qice_tot', 'poro_tot', 'density', 'info']
                    for attr in attrs:
                        if hasattr(mat, attr):
                            _save_attr(mat_grp, attr, getattr(mat, attr))
                    
                    # Save datasets
                    if hasattr(mat, 'wavs') and mat.wavs is not None:
                        mat_grp.create_dataset('wavs', data=mat.wavs)
                    if hasattr(mat, 'eps') and mat.eps is not None:
                        # Complex numbers handling: save real and imag parts
                        mat_grp.create_dataset('eps_real', data=mat.eps.real)
                        mat_grp.create_dataset('eps_imag', data=mat.eps.imag)

    def save_beta_csv(self, file_name, include_Qpr_star_avg=False):
        """
        Save beta values to a CSV file.

        The default output has two columns:
        diameter_um,beta

        If include_Qpr_star_avg is True, the stellar-spectrum-averaged Qpr is
        included as a third column:
        diameter_um,beta,Qpr_star_avg
        
        Args:
            file_name (str): Path to the CSV file to create.
            include_Qpr_star_avg (bool, optional): Include Qpr_star_avg as an
                additional column. Defaults to False.
        """
        if self.prtl is None or getattr(self.prtl, 'betas', None) is None:
            raise ValueError("Particles with computed betas are required to save beta CSV.")

        diams = np.asarray(self.prtl.diams)
        betas = np.asarray(self.prtl.betas)

        if diams.shape != betas.shape:
            raise ValueError("'diams' and 'betas' must have the same shape.")

        columns = [diams, betas]
        header = ["diameter_um", "beta"]

        if include_Qpr_star_avg:
            Qpr_star_avg = getattr(self.prtl, 'Qpr_star_avg', None)
            if Qpr_star_avg is None:
                raise ValueError(
                    "Qpr_star_avg is required when include_Qpr_star_avg=True. "
                    "Run calculate_Qpr_star_avg() or calculate_beta_factors() first."
                )

            Qpr_star_avg = np.asarray(Qpr_star_avg)
            if diams.shape != Qpr_star_avg.shape:
                raise ValueError("'diams' and 'Qpr_star_avg' must have the same shape.")

            columns.append(Qpr_star_avg)
            header.append("Qpr_star_avg")

        data = np.column_stack(columns)

        with open(file_name, 'w', newline='') as file:
            # Using comma-separated fixed-width fields for human readability while maintaining
            # compatibility with the Julia loader (which splits by comma and strips whitespace).
            fmt = "%.7e"
            text_columns = [
                [fmt % value for value in data[:, col_idx]]
                for col_idx in range(data.shape[1])
            ]
            widths = [
                max(len(header[col_idx]), *(len(value) for value in text_columns[col_idx]))
                for col_idx in range(data.shape[1])
            ]
            widths[0] = max(widths[0], len("# ") + len(header[0]))

            header_line = "# " + header[0]
            for col_idx, label in enumerate(header[1:], start=1):
                previous_width = widths[col_idx - 1]
                if col_idx == 1:
                    previous_width -= len("# ")
                header_line += "," + " " * (previous_width - len(header[col_idx - 1]) + 1) + label
            file.write(header_line + "\n")

            for row in zip(*text_columns):
                file.write(", ".join(
                    value.rjust(widths[col_idx])
                    for col_idx, value in enumerate(row)
                ).rstrip() + "\n")

    def save_qabs_bnu_hdf5(self, file_name):
        """
        Save the emissivity-weighted Planck function (Qabs * B_nu) to an HDF5 file.
        
        The 3D array has dimensions (dists, diams, wavs). Labels and values for 
        each axis are stored as separate datasets and attributes.
        
        Args:
            file_name (str): Path to the HDF5 file to create.
        """
        if self.prtl is None or getattr(self.prtl, 'bnus', None) is None or getattr(self.prtl, 'Qabs', None) is None:
            raise ValueError("Particles with computed Qabs and bnus are required.")

        # Qabs is (n_diams, n_wavs), bnus is (n_dists, n_diams, n_wavs)
        qabs_bnu = self.prtl.Qabs[np.newaxis, :, :] * self.prtl.bnus
        
        with h5py.File(file_name, 'w') as f:
            dset = f.create_dataset('Qabs_Bnu', data=qabs_bnu)
            dset.attrs['dimensions'] = ['dists', 'diams', 'wavs']
            dset.attrs['units'] = 'Jy/sr' # bnus defaults to frequency domain (Jy/sr)
            
            # Store axis values
            f.create_dataset('dists', data=self.prtl.dists)
            f.get('dists').attrs['units'] = 'au'
            
            f.create_dataset('diams', data=self.prtl.diams)
            f.get('diams').attrs['units'] = 'um'
            
            f.create_dataset('wavs', data=self.prtl.wavs)
            f.get('wavs').attrs['units'] = 'um'

    @staticmethod
    def load(file_name):
        """Load a complete result from a file.
        
        After loading, you can access:
            result.star - The star configuration
            result.prtl - The Particles object with all properties
            result.prtl.matrl - The material properties
        """
        with open(file_name, 'rb') as file:
            return pickle.load(file)


# Backwards-compatible name retained for existing scripts and pickle files.
OpticalModel = SystemResult
