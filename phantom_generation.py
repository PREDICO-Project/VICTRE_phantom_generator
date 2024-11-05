
from Victre import Pipeline
from Victre import Constants
import os
import sys
import random
# Script used to generate VICTRE's phantom with some preset parameters
class Generation():

    def __init__(self):
        # Select which processes are done
        self.generate_phantom = True # Breast Generation True/False
        self.compress_phantom = True # Breast Compression True/False
        self.lesion = True # Lesion Insertion True/False
        self.projection = True # MCGPU Projection True/False
        self.reconstruction = False # Reconstruction of Projections True/False
        

        # Set some important parameters
        self.seed = random.randint(1, 9999) # Random seed
        self.results_folder = "results/Scattered_calc" # Path to Results folder, can be modified
        os.makedirs(self.results_folder, exist_ok =True) # If folder does not exists, it will be created
        self.breast_type = "Scattered" # Dense, Fatty, Heterogeneous, Scattered
        self.imgRes = 0.2 # Voxel Size in mm
        
        
        # Set some paths to existing phantoms (if exists)
        self.phantom_file = "phantoms/Heterogeneous_lession.raw" # Just in case you don´t want to generate the phantom and select an existing one
        self.compressed_phantom = "PATH_TO_COMPRESSED_MHD" # Must be modified
        
        self.lesion_type = 'calc' # calc or mass
		
		# Set arguments for mcgpu
        self.events = 2.3877e11
        self.number_projections = 0
        self.spectrum_file= "./Victre/projection/spectrum/W30kVp_Rh50um_Be1mm.spc"
        
        self.roi_sizes = {Constants.VICTRE_SPICULATED: [65, 65, 5],
             Constants.VICTRE_CLUSTERCALC: [65, 65, 5]} # Can be modified
        
        if self.lesion:
            if self.lesion_type == 'mass':
                self.lesion_file = "lesions/spiculated/mass_11_size1.00.h5" # Can be modified
                
            if self.lesion_type == 'calc':
                self.lesion_file = "lesions/clustercalc/clustercalc_model.h5" # Can be modified
                
		
        self.arguments_mcgpu = {
            "number_projections": self.number_projections,
            "number_histories": self.events,
            "spectrum_file": self.spectrum_file} # More attributes can be added
        
        self.arguments_generation = self.define_arguments_from_Constants() # define_arguments_from_Constants() or define_arguments_manually()

        # Set arguments_generation directly, without running the method define_arguments_from_Constants() nor define_arguments_manually()
        # See https://didsr.github.io/VICTRE_PIPELINE/advanced.html to check all parameters that can be added or modified
        """self.arguments_generation = {

            "compressionThickness": 60,  # mm

            # phantom voxel size (mm)
            "imgRes": self.imgRes,

            # desired fat fraction
            "targetFatFrac": 0.5 
        }"""
        ##########################################
        # DO NOT MODIFY ANY LINE FROM THIS POINT #
        ##########################################
        
        self.arguments_generation["imgRes"] = self.imgRes
        print(self.arguments_generation)
        
        pline = self.define_Pipeline()

        if self.generate_phantom:
            pline.generate_phantom()
        
        if self.compress_phantom:
            pline.compress_phantom()

        if self.lesion:
            if self.lesion_type == 'mass':
                
                pline.insert_lesions(lesion_type=Constants.VICTRE_SPICULATED,
                            n=3)
            if self.lesion_type == 'calc':
                
                pline.insert_lesions(lesion_type=Constants.VICTRE_CLUSTERCALC,
                            n=3)
        if self.projection:
            pline.project()
            pline.save_DICOM("dm")

        if self.reconstruction:    
            pline.reconstruct()
            pline.save_DICOM("dbt")
            #pline.save_DICOM("dm")

    def define_arguments_from_Constants(self):

        if self.breast_type == 'Fatty':
            arguments_generation = Constants.VICTRE_FATTY
            

        if self.breast_type == 'Dense':
            arguments_generation = Constants.VICTRE_DENSE
        
        if self.breast_type == 'Scattered':
            arguments_generation = Constants.VICTRE_SCATTERED
        
        if self.breast_type == 'Heterogeneous':
            arguments_generation = Constants.VICTRE_HETERO
        

        return arguments_generation
    def define_arguments_manually(self):
        # If want to add more parameters, modify the arguments_generation dictionary
        # Set parameters for each type of breast

        if self.breast_type == "Fatty":
            targetFatFrac = 0.548
            compressionThickness = 60
            
        if self.breast_type == "Dense":
            targetFatFrac = 0.071
            compressionThickness = 35
		
        if self.breast_type == "Scattered":
            targetFatFrac = 0.339
            compressionThickness = 55
        
        if self.breast_type == "Heterogeneous":
            targetFatFrac = 0.143
            compressionThickness = 45
        

        arguments_generation = {
            "compressionThickness": compressionThickness,  # mm
            # phantom voxel size (mm)
            "imgRes": self.imgRes,
            # desired fat fraction
            "targetFatFrac": targetFatFrac
            }
        return arguments_generation
    
                
    def define_Pipeline(self):
        # If lesion are inserted
        if self.lesion:
            
            if self.generate_phantom:
                pline = Pipeline(results_folder = self.results_folder,
                    seed = self.seed,
                    lesion_file=self.lesion_file, 
                    arguments_generation = self.arguments_generation,
                    roi_sizes=self.roi_sizes,
                    arguments_mcgpu=self.arguments_mcgpu)
            else:
                pline = Pipeline(results_folder = self.results_folder,
                    seed = self.seed,
                    phantom_file=self.phantom_file,
                    lesion_file=self.lesion_file,
                    roi_sizes=self.roi_sizes,
                    arguments_mcgpu=self.arguments_mcgpu)

        
        if self.lesion == False:
            if self.generate_phantom:
                pline = Pipeline(results_folder = self.results_folder,
                        seed = self.seed,
                        arguments_generation = self.arguments_generation,
                        arguments_mcgpu=self.arguments_mcgpu)
            else:
                pline = Pipeline(results_folder = self.results_folder,
                    seed = self.seed,
                    phantom_file=self.phantom_file,
                    arguments_mcgpu=self.arguments_mcgpu)

        return pline
            
       

run = Generation()


