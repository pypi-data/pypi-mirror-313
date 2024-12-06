import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import tables
from tables.exceptions import NoSuchNodeError
import astropy.units as u
import astropy.constants as c
from .import_config import import_config, eval_kwargs
from .chemistry_properties import *

# Some defaults for labelling on plots.
cb_label_size = 14
axis_label_size = 16

# A few default values for functions.
NGRAIN = 128
NZ = 32
NCHEM = len(molecule_array)
LEVELS = np.arange(-27, -10, 2)              # Levels for 2D plot of dus and gas mass densities
ICE_NUBER_LEVELS = np.arange(-100, 0, 5)    # Levels for 2D plot of ice number densities
GAS_NUMBER_LEVELS = np.arange(-20, 14, 1)   # Levels for 2D plot of gas number densities

# Colour map from Dr Adrien Houge
HUGE_CMAP_LIST = ['#EDE0D4', '#E6CCB2', '#DDB892', '#B08968', '#7F5539', '#9C6644']
HUGE_CMAP = LinearSegmentedColormap.from_list("Cmap", HUGE_CMAP_LIST, N = 200)

def instructions():
    '''
    Function you can call to learn what to do with this module.
    '''
    print("\n\
    Create a Python file in the same folder as your simulation .h5 file and config file.\n\
    Then in the Python file, import the Disc_class module and instantiate the class as:\n\
    \n\
        from disc_loader import Disc_class\n\
        Disc = Disc_class('simulation.h5', 'config.yaml')\n\
    \n\
    Parameters can be accessed via class attributes, e.g:\n\
        sigma_gas   = Disc.sigma_g          # Retrieves gas surface density\n\
        CO_gas      = Disc.gas.CO           # Retrieves CO vapour surface density\n\
        Water_ice   = Disc.dust.H2O         # Retrieves water icte surface density\n\
        ")
    

class Disc_class:
    '''
    Class object that stores all the disc data and some methods to perform
    certain actions with the data (e.g. plotting, calculations, 2D stuff etc.)

    '''
    def __init__(self, file_path, config_file_path):
        self.initialise_constants()
        self.load_disc(file_path)
        self.load_parameters_from_config(config_file_path)
        self.gas    = Disc_gas(self)
        self.dust   = Disc_dust(self)

    def initialise_constants(self):
        self.AU     = (1*u.au).cgs.value    # define the astronomical unit conversion from cgs
        self.Myr    = (1*u.Myr).cgs.value   # define the Megayear unit conversion from cgs
        self.k_b    = c.k_B.cgs.value       # boltzmann constant
        self.m_p    = c.m_p.cgs.value       # proton mass
        self.G      = c.G.cgs.value         # gravitational constant
        self.Msun   = c.M_sun.cgs.value     # solar mass
        self.Mearth = c.M_earth.cgs.value   # earth mass
        self.COtemp             = iceline_temperatures[0]
        self.N2temp             = iceline_temperatures[0]
        self.CH4temp            = iceline_temperatures[1]
        self.CO2temp            = iceline_temperatures[2]
        self.NH3temp            = iceline_temperatures[3]
        self.trapped_CO_temp    = iceline_temperatures[4]
        self.H2Otemp            = iceline_temperatures[4]
        self.Fe3O4temp          = iceline_temperatures[5]
        self.Ctemp              = iceline_temperatures[6]
        self.FeStemp            = iceline_temperatures[7]
        self.NaAlSi3O8          = iceline_temperatures[8]
        self.KAlSi3O8temp       = iceline_temperatures[9]
        self.Mg2SiO4temp        = iceline_temperatures[10]
        self.Fe2O3temp          = iceline_temperatures[11]
        self.VOtemp             = iceline_temperatures[12]
        self.MgSiO3temp         = iceline_temperatures[13]
        self.Al2O3temp          = iceline_temperatures[14]
        self.TiOtemp            = iceline_temperatures[15]


    def load_disc(self, file_path):
        '''
        Function that loads the disc from the .h5 file produced by chemcomp simulations.
        Saves each disc parameter in a class attribute.

        NOTE:
            self.r is rescaled from cgs to AU.
            self.t is rescaled from cgs to Myr.

        Inputs:
            file_path : path to the .h5 file relative to the current folder. Includes the .h5 file
        '''

        # Load quantities
        with tables.open_file(file_path, mode='r') as f:
            self.disc_quantities = [q for q in dir(f.get_node('/disk')) if q[0]!='_']

            self.T                       = np.array(f.root.disk.T)                       # Disc temperature
            self.T_irr                   = np.array(f.root.disk.T_irr)                   # Disc temperature due to stellar radiation
            self.T_visc                  = np.array(f.root.disk.T_visc)                  # Disc temperature due to viscous heating
            self.a_1                     = np.array(f.root.disk.a_1)                     # 
            self.cum_pebble_flux         = np.array(f.root.disk.cum_pebble_flux)         # Cumulative pebble flux
            self.f_m                     = np.array(f.root.disk.f_m)                     # 
            self.m_dot                   = np.array(f.root.disk.m_dot)                   # Gas accretion rate
            self.m_dot_components        = np.array(f.root.disk.m_dot_components)        # Gass accretion rate for each species
            self.mu                      = np.array(f.root.disk.mu)                      # Mean molecular weight
            self.peb_iso                 = np.array(f.root.disk.peb_iso)                 # Pebble isolation mass at disc positions
            self.pebble_flux             = np.array(f.root.disk.pebble_flux)             # Pebble flux due to all pebbles
            self.r                       = np.array(f.root.disk.r) / self.AU                  # Radial grid
            self.r_i                     = np.array(f.root.disk.r_i)                     #
            self.sigma_dust              = np.array(f.root.disk.sigma_dust)              # Dust & ice surface density
            self.sigma_dust_components   = np.array(f.root.disk.sigma_dust_components)   # Dust & ice surface density for each species/element
            self.sigma_g                 = np.array(f.root.disk.sigma_g)                 # Gas surface density
            self.sigma_g_components      = np.array(f.root.disk.sigma_g_components)      # Gas surface density for each species/element
            self.stokes_number_df        = np.array(f.root.disk.stokes_number_df)        # Stokes number in drift-induced fragmentation limit
            self.stokes_number_drift     = np.array(f.root.disk.stokes_number_drift)     # Stokes number in drift-limit
            self.stokes_number_frag      = np.array(f.root.disk.stokes_number_frag)      # Stokes number in fragmentation limit
            self.stokes_number_pebbles   = np.array(f.root.disk.stokes_number_pebbles)   # Stokes number of large dust population
            self.stokes_number_small     = np.array(f.root.disk.stokes_number_small)     # Stokes number of small dust population
            self.t                       = np.array(f.root.disk.t)  / self.Myr                 # Time grid
            self.vr_dust                 = np.array(f.root.disk.vr_dust)                 # Radial velocity of dust
            self.vr_gas                  = np.array(f.root.disk.vr_gas)                  # Radial velocity of gas
            try:
                self.lstar               = np.array(f.root.disk.lstar)
            except NoSuchNodeError:
                print('No \'lstar\' parameter found.')
            try:
                self.rho_solid           = np.array(f.root.disk.rho_solid)
                self.rho_solid = self.rho_solid[0,-1]
            except NoSuchNodeError:
                print('No \'rho_solid\' parameter found. Using config file value.')
    

    def load_parameters_from_config(self, config_file_path):
        '''
        Function that loads the disc parameters from the config file.
        
        Some code for this function taken straight from the chemcomp files. (https://github.com/AaronDavidSchneider/chemcomp)
        Code taken straight from `/chemcomp/chemcomp/helpers/main_helpers.py
        Full credit to Aaron David Schneider & Betram Bitsch.
        '''
        config                  = import_config(config_file_path)
        defaults                = config.get("defaults", {})
        config_disk             = config.get("config_disk", {})
        config_pebble_accretion = config.get("config_pebble_accretion", {})
        config_gas_accretion    = config.get("config_gas_accretion", {})
        config_planet           = config.get("config_planet", {})
        output                  = config.get("output", {})
        chemistry_conf          = config.get("chemistry", {})

        # Evaluating chemical partitioning model initial conditions
        self.chemistry = Disc_chemistry(chemistry_conf)

        # Evaluating disc and pebble parameters
        self.M_star             = eval_kwargs(config_disk.get('M_STAR', None))
        self.alpha              = eval_kwargs(config_disk.get('ALPHA', None))
        self.alpha_height       = eval_kwargs(config_disk.get('ALPHAHEIGHT', None))
        self.Mdisk              = eval_kwargs(config_disk.get('M0', None))
        self.Rdisk              = eval_kwargs(config_disk.get('R0', None))
        self.DTG                = eval_kwargs(config_disk.get('DTG_total', None))
        self.static             = eval_kwargs(config_disk.get('static', None)) # gas/dust evolution boolean
        self.evaporation        = eval_kwargs(config_disk.get('evaporation', None))
        self.static_stokes      = eval_kwargs(config_disk.get('static_stokes', None))
        self.tau_disk           = eval_kwargs(config_disk.get('tau disk', None))
        self.begin_photevap     = eval_kwargs(config_disk.get('begin_photevap', None))
        self.temp_evol          = eval_kwargs(config_disk.get('temp_evol', None))
        self.evap_width         = eval_kwargs(config_disk.get('evap_width', None))
        self.vfrag              = eval_kwargs(config_pebble_accretion.get('u_frag', '1m/s for dry, 10m/s for icy pebbles'))
        
        if not hasattr(self, 'rho_solid'): # Only if rho_solid has been set in config file
            self.rho_solid          = eval_kwargs(config_pebble_accretion.get('rho_solid'))
            if self.rho_solid is None:
                print('No \'rho_solid\' parameter found in config or output. Assuming rho=1.67 g/cm^3 for grain size calculations.')
                self.rho_solid = 1.67
    

    def calculate_C_to_O(self, t=None):
        '''
        Function to calculate the C-to-O ratio in the disc for the solid and gas
        phases.
        '''
        self.dust.C_to_O    = self.dust.C_elem / self.dust.O * 16/12
        self.gas.C_to_O     = self.gas.C_elem / self.gas.O * 16/12
    
    def calculate_O_to_H(self):
        if t == None:
            print('No time specified to C/O ratio. Assuming t = 1 Myr.')
            t = 1
        self.it = self.t.searchsorted(t)
        self.dust.O_to_H    = self.dust.O / self.dust.H * 1/16
        self.gas.O_to_H     = self.gas.O / self.gas.H * 1/16

    def calculate_2D(self, time=None, ngrain=NGRAIN, nchem=NCHEM, nz=NZ, summed=True):
        '''
        Function that calculates 2D distributions of dust, ice, gas and vapour.
        '''
        if time == None:
            print('Time for 2D distributions not specified, assuming t = 1 Myr')
            time = 1
        self.it = self.t.searchsorted(time)

        # Calculating grain sizes from chemcomp outputs
        self.grains   = (2/np.pi) * self.sigma_g[self.it, :] * self.stokes_number_small[self.it, :] / self.rho_solid
        self.pebbles = (2/np.pi) * self.sigma_g[self.it, :] * self.stokes_number_pebbles[self.it,   :] / self.rho_solid

        len_r = len(self.r)
        self.grain_sizes         = np.zeros((len_r, ngrain))        # grain sizes at all radii for chemcomp
        self.size_distr_arr      = np.zeros((len_r, ngrain))        # number distribution at all radii
        self.surface_density_arr = np.zeros((len_r, ngrain))        # surface density at all radii for each grain family
        self.molecule_sigma_arr  = np.zeros((len_r, ngrain, nchem)) # surface density for all the molecular species

        '''
        IMPORTANT NOTE
        The way I hvae written this means that there are ngrain grain families at every radius. This makes
        the arrays extremely easy to handle, because there's the same number of grain families for all r.

        However, this means you CANNOT plot e.g. the surface density to 1cm-sized grains.
        I don't think that this is mega important right now. It does make it a bit skewed for DALI-related
        stuff, as you sometimes have e.g. 15 grain families below 1 micron, and sometimes 40 below 1 micron.
        
        Having said that, this approach I've written works great for generating 2D plots, but I don't think 
        it's of any consequence right now, even for DALI-related stuff. It could be for opacity things, 
        but we can fix it for that (:
        '''

        # Global maximum
        max_grain_size = np.max(self.pebbles)
        # s_min_cc = np.min(pebbles_cc)
        # s_min_cc = np.min(grain_cc)                                                          # Smallest grain size in DALI
        s_min = 5e-7
        print(f'Global maximum: {max_grain_size:.4e}')
        print(f'Global minimum: {s_min:.4e}')
        sizes = np.logspace(np.log10(s_min), np.log10(max_grain_size), ngrain)   # Size distribution to find dlog(s)
        dlogs = np.median( np.diff( np.log10(sizes) ) )                             # Constant dlog(s) to use with every size distribution
        ratio = 10**dlogs

        for i in range( len_r ):
            # Grabbing surface density to calculate n0 with
            sigma_for_n0 = self.sigma_dust[self.it, i]
            sigma_ice_for_n0 = self.sigma_dust_components[self.it, i, 1, :]

            local_maximum = np.maximum(self.pebbles[i], s_min) # max grain size from twopoppy
            print(f'Local maximum: {local_maximum:.4e}')
            
            # Generate arrays of grain sizes up to the maximum, and 0 beyond that
            geometric_grains = self.geo_array_to_maximum(s_min, ratio, local_maximum, ngrain)
            self.grain_sizes[i, :len(geometric_grains)] = geometric_grains

            # power for the size distribution
            q = -3.5
            
            # Calculating normalisation factors
            n0      = self.calc_n0(q, sigma_for_n0, dlogs, self.grain_sizes[i,:])
            n0_ice  = self.calc_n0(q, sigma_ice_for_n0, dlogs, self.grain_sizes[i,:])
            
            # Size distributions
            size_distr = n0 * self.grain_sizes[i,:] **(q)                        # Dust grains
            size_distr_ice = n0_ice[:,None] * self.grain_sizes[None,i,:] ** q    # Ice grains; vectorized

            # Calculating surface density due to each of the grain sizes
            sigma_size_distr = size_distr * (4/3) * np.pi * self.rho_solid * self.grain_sizes[i,:]**4 * dlogs
            sigma_ice_distr   = size_distr_ice * (4/3) * np.pi * self.rho_solid * self.grain_sizes[i,:]**4 * dlogs

            #### Sanity checks ####
            #   Loop for ice grain sizes
            temp = np.zeros((19, ngrain))
            for f, n in enumerate(n0_ice):
                temp[f,:] =  n * self.grain_sizes[i,:] ** q
            if temp.all() != size_distr_ice.all():
                print('ERROR: Vectorized ice size distribution calculation is wrong!')

            assert temp.all() == size_distr_ice.all(), f'Vectorized ice size distribution calculation is wrong! Loop #{i} -> r = {r[i]:.1f} AU'

            #   Loop for ice grain surface density
            what_the_sigma = np.zeros((ngrain, nchem))
            for x, sizes in enumerate(size_distr_ice):
                what_the_sigma[:,x] = sizes * (4/3) * np.pi * self.rho_solid * self.grain_sizes[i,:]**4 * dlogs
            
            if what_the_sigma.all() != sigma_ice_distr.all():
                print('ERROR: Vectorized ice surface density calculation is wrong!')
            assert what_the_sigma.all() == sigma_ice_distr.all(), 'Vectorized ice surface density calculation is wrong!'
            
            # Comparing against original Chemcomp surface density
            # It's necessary the sum over grain sizes returns exactly the surface density
            if not np.isclose( np.nansum(sigma_size_distr), sigma_for_n0):
                print('SHIT ON IT - recalculated sigma is wrong!')
                # print(sigma_size_distr)
                print(f'Recalculated sigma: {np.nansum(sigma_size_distr)}')
                print(f'Original sigma:     {sigma_for_n0}')
                print(f'Loop: {i}')
                break

            # Saving calculations to arrays
            self.size_distr_arr[i, :] = size_distr               # number of particles per cm^2 for a given size
            self.surface_density_arr[i, :] = sigma_size_distr    # dust surface density for a given size
            self.molecule_sigma_arr[i, :, :] = sigma_ice_distr.T    # ice surface densities for a given size

        # Other skibidi garbage to produce the 2D plot
        omegaK = np.sqrt( (self.G * self.M_star * self.Msun) / (self.r*self.AU)**3 )
        cs = np.sqrt(self.k_b*self.T[self.it, :]/(2.3*self.m_p)) # sound speed                                                                          
        gas_scale_height = cs / omegaK
        

        # Distribution of Stokes Numbers for different grain sizes at all radii
        temp = np.zeros((len_r, ngrain))
        for i in range(ngrain):
            temp[:,i] = (np.pi / 2) * self.rho_solid * self.grain_sizes[:,i] / self.sigma_g[self.it,:] 

        stokes_distr = ( (np.pi / 2) * self.rho_solid * self.grain_sizes[:,:].T / self.sigma_g[self.it,:] ).T

        if temp.all() != stokes_distr.all():
            print('Stokes wrong!')
        assert temp.all() == stokes_distr.all(), 'ERROR: Vectorized Stokes calculation is incorrect!'

        # pebble scale height at all radii for all grain families
        pebble_scale_height = np.zeros((len_r, ngrain))

        for i in range(ngrain):     # again, could be vectorised, but runs quick enough
            denominator = np.zeros(len_r)

            for k, St in enumerate( stokes_distr[:, i] ):
                denominator[k] = (1 + St**2) * np.minimum(St, 0.5)
            pebble_scale_height[:, i] = gas_scale_height * np.minimum(1, np.sqrt(self.alpha_height / denominator ) )

        # Generating z/r arrays. God help me these do not make sense but they work
        z_over_r_cc = np.linspace(0, 0.8, nz) # z/r array
        self.z = z_over_r_cc * self.r[:, None]
        self.rho_dust = np.zeros((len_r, nz, ngrain))          # 2D dust+ice mass density array
        self.rho_gas  = np.zeros((len_r, nz))                  # 2D gas mass density array
        self.rho_ice = np.zeros((len_r, nz, ngrain, nchem))    # 2D ice mass density array for each volatile
        self.rho_vapour  = np.zeros((len_r, nz, nchem))        # 2D volatile vapour mass density array

        # Calculating vertical densities
        # Loops over z (which is the same as looping over constant z/r lines). Could be vectorised, but is quick enough!
        for i, z in enumerate(self.z.T):
            # H = gas_scale_height # for swapping the gas and pebble scale heights
            gas_exponent = np.exp( - z**2 / (2 * (gas_scale_height / self.AU)**2) ) # converting gas scale height to AU
            self.rho_gas[:, i]  = self.sigma_g[self.it,:] / (np.sqrt(2 * np.pi) * gas_scale_height) * gas_exponent

            # Calculating volatile vapour densities
            for v in range(nchem):
                self.rho_vapour[:, i, v-1] = self.sigma_g_components[self.it, : , 1, v] / (np.sqrt(2 * np.pi) * gas_scale_height) * gas_exponent

            # Looping over grain sizes for dust and ice
            for j in range(ngrain):
                H = pebble_scale_height[:,j]

                sigma = self.surface_density_arr[:,j] # what the sigma

                exponent = np.exp( - z**2 / (2 * (H / self.AU)**2) ) # converting pebble scale height to AU
                rho_dust = sigma / (np.sqrt(2 * np.pi) * H) * exponent
                self.rho_dust[:, i, j] = rho_dust

                # Vertical densities for ice species    
                for k in range(nchem):
                    sigma_ice = self.molecule_sigma_arr[:, j, k-1]
                    rho_ice = sigma_ice / (np.sqrt(2 * np.pi) * H) * exponent
                    self.rho_ice[:, i, j, k-1] = rho_ice
        
        if summed:
            # Summing over all dust sizes to get net contributions
            self.rho_dust = np.nansum(self.rho_dust, axis=2)
            self.rho_ice = np.nansum(self.rho_ice, axis=2)

            # Setting a floor
            self.rho_ice = np.where(self.rho_ice == 0, 1e-50, self.rho_ice)
            self.rho_dust = np.where(self.rho_dust == 0, 1e-50, self.rho_dust)


    
    def calc_n0(self, q, Sigma, dlogs, s_centre):
     '''
     Function that calculates the normalising constant buried within the grain size distribution:
        n(s)ds = n0 * s^(-3.5) * ds
    
    Returns:
        n0 : normalising constant for above equation
     '''
     return (3 * Sigma) / (4 * np.pi * self.rho_solid * dlogs * np.nansum(s_centre ** (q+4)))


    def find_n(self, init, ratio, max, ngrain):
        '''
        Function that finds n such that:
            init * ratio ** n = s
        Always rounds down due to Python's int() function [intended].
        '''
        return np.minimum( int( np.log10(max/init) / np.log10(ratio) ), ngrain)


    def geo_array(self, init, ratio, N_geo):
        '''
        Function that calculates geometric progression from init with ratio for a set number of
        array elements. I.e.
            init * ratio ** n
        where 0 ≤ n ≤ N_geo.
        
        Returns:
            array of geometric progression
        '''
        return np.array([init * ratio ** n for n in range(N_geo+1)])


    def geo_array_to_maximum(self, init, ratio, max, ngrain):
        '''
        Function that calculates a geometric progression until a maximum number for a set ratio.
        Like np.arange and np.logspace, but combined so you can define the ratio in logspace
        (analogously to dx in np.arange).

        Inputs:
            init : initial value for geometric progression
            ratio : ratio used in the geometric progression
            max : maximum value to which to calculate the geometric progression
        Returns:
            array of geometric progression
        '''
        N_geo = self.find_n(init, ratio, max, ngrain)
        return self.geo_array(init, ratio, N_geo)






    

    def plot_2D_distribution(self,
                             distribution=None,
                             time=None,
                             levels=None, 
                             figure=None, 
                             axis=None,
                             cmap=HUGE_CMAP, 
                             extend='both', 
                             cb_label=None):
        if figure is None:
            figure = plt.figure()
        if axis is None:
            axis = figure.gca()
        
        if distribution is None:
            print('No distribution provided. Using dust density distribution.')
            distribution = self.rho_dust
            cb_label = '$\\log_{10}([\\rho_{\\rm{dust}} + \\rho_{\\rm{ice}}] / \\rm{gcm}^{-2} )$'

        if levels is None:
            levels = LEVELS

        if time == None:
            print('Time for 2D distributions not specified, assuming t = 1 Myr')
            time = 1
        self.it = self.t.searchsorted(time)

        two_dee_plot = axis.contourf(self.r, (self.z/self.r[:,None])[0], np.log10( distribution ).T,
                                     levels=levels,
                                     extend=extend,
                                     cmap=cmap)
        cb = figure.colorbar(two_dee_plot)
        cb.ax.set_ylabel(cb_label, fontsize=cb_label_size)
        axis.set_xlabel('$r$ (AU)', fontsize=axis_label_size)
        axis.set_ylabel('$z/r$', fontsize=axis_label_size)
        axis.set_xscale('log')
        figure.set_tight_layout(True)
        return figure, axis

        
class Disc_gas:
    '''
    Class that contains the gas surface densities of the disc.
    Attributes can be accessed via e.g. self.gas.CO inside Disc_class.
    '''
    def __init__(self, super):
        # Disc_gas does not need to inherit any components of super.
        # Elemental distributions
        for element, gas_component in zip(element_array,
                                          super.sigma_g_components[:,:,0,:].swapaxes(0,2).swapaxes(1,2)):
            setattr(self, element, gas_component)        

        # Molecules
        for molecule, gas_component in zip(molecule_array,
                                           super.sigma_g_components[:,:,1].swapaxes(0,2).swapaxes(1,2)):
            setattr(self, molecule, gas_component)


class Disc_dust:
    '''
    Class that contains the dust and ice surface densities of the disc.
    Attributes can be accessed via e.g. self.dust.CO inside Disc_class.
    '''
    def __init__(self, super):
        # Elemental distributions
        for element, gas_component in zip(element_array,
                                          super.sigma_dust_components[:,:,0].swapaxes(0,2).swapaxes(1,2)):
            setattr(self, element, gas_component)        

        # Molecules
        for molecule, gas_component in zip(molecule_array,
                                           super.sigma_dust_components[:,:,1].swapaxes(0,2).swapaxes(1,2)):
            setattr(self, molecule, gas_component)


class Disc_chemistry:
    def __init__(self, chemistry_conf):
        '''
        Note that this assumes use_FeH = False.

        Some code for this function taken straight from the chemcomp files. (https://github.com/AaronDavidSchneider/chemcomp)
        Code taken straight from `/chemcomp/chemcomp/disks/_chemistry.py
        Credit to Aaron David Schneider & Betram Bitsch.
        '''
        self.OH         = OH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('OH',   0.0 )))
        self.CH         = CH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('CH',   0.0 )))
        self.SiH        = SiH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('SiH',  0.0 )))
        self.SH         = SH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('SH',   0.0 )))
        self.MgH        = MgH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('MgH',  0.0 )))
        self.FeH        = FeH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('FeH',  0.0 )))
        self.NH         = NH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('NH',   0.0 )))
        self.AlH        = AlH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('AlH',  0.0 )))
        self.TiH        = TiH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('TiH',  0.0 )))
        self.KH         = KH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('LH',   0.0 )))
        self.NaH        = NaH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('NaH',  0.0 )))
        self.VH         = VH_init_abu   * 10 ** (eval_kwargs(chemistry_conf.get('VH',   0.0 )))
        self.HeH        = HeH_init_abu  * 10 ** (eval_kwargs(chemistry_conf.get('HeH',  0.0 )))
        self.C_frac     = eval_kwargs(chemistry_conf.get('C_frac', 0.2))
        self.CH4        = eval_kwargs(chemistry_conf.get('CH4_frac', (0.45 - self.C_frac)))
        self.CO_frac    = eval_kwargs(chemistry_conf.get('CO_frac', 0.45))
        self.CO2_frac   = eval_kwargs(chemistry_conf.get('CO2_frac', 0.1))
