from pathlib import Path
import numpy as np
import astromiedust as amd

script_dir = Path(__file__).parent

# --------------------------- Setup test parameters -----------------------------
# Create star object with Fomalhaut parameters
star = amd.Star(name='Fomalhaut', lum_suns=16.6, mass_suns=1.92,
    spectrum_file=script_dir / 'fomalhaut_spectrum.txt')

# Create material object example volume fractions of silicate, ice, and voids
matrl = amd.Material(qsil=.4, qice=1.0, mpor=.7, emt='maxwell-garnett')

wavs = np.logspace(0, 4, 300)
diams = np.logspace(0, 4, 41)
dists = np.logspace(0, 3, 43)

# --------------------------- Calculate optical properties -----------------------
# Create Particles instance and calculate all properties
prtl = amd.Particles(diams=diams, wavs=wavs, dists=dists,
                     matrl=matrl, suppress_mie_resonance=True)
prtl.calculate_all(star)

# --------------------------- Save complete state --------------------------------
model = amd.OpticalModel(star=star, prtl=prtl)
model.save(script_dir / 'fomalhaut_results.pkl')
# model.save_beta_csv(script_dir / 'fomalhaut_beta.csv')
# model.save_qabs_bnu_hdf5(script_dir / 'fomalhaut_therm_emission.h5')



# ----------------------------- Later, load and use: -------------------------------
# loaded_model = amd.OpticalModel.load(script_dir / 'fomalhaut_results.pkl')
# prtl = loaded_model.prtl
# star = loaded_model.star

# Make a few plots:
savefig_kwargs = dict(dpi=300, bbox_inches='tight', pad_inches=0.01)
ax0 = star.plot_spectrum()    
ax0.figure.savefig(script_dir / 'star_spectrum.png', **savefig_kwargs)
ax1 = prtl.plot_Q(diams = np.logspace(1,3,5), Q_type='abs')
ax1.figure.savefig(script_dir / 'Qabs.png', **savefig_kwargs)
ax1 = prtl.plot_Q(diams = np.logspace(1,3,5), Q_type='sca')
ax1.figure.savefig(script_dir / 'Qsca.png', **savefig_kwargs)
ax1 = prtl.plot_Q(diams = np.logspace(1,3,5), Q_type='pr')
ax1.figure.savefig(script_dir / 'Qpr.png', **savefig_kwargs)
ax2 = prtl.plot_beta()
ax2.figure.savefig(script_dir / 'beta.png', **savefig_kwargs)
ax3 = prtl.plot_temp()
ax3.figure.savefig(script_dir / 'temp.png', **savefig_kwargs)
ax4 = prtl.plot_g(diams = np.logspace(1,3,5))
ax4.figure.savefig(script_dir / 'g.png', **savefig_kwargs)
