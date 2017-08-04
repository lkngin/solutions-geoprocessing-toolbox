# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
CountIncidentsByLOCTestCase.py
--------------------------------------------------
requirments: ArcGIS X.X, Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
history:
12/16/2015 - JH - initial creation
09/20/2016 - MF - Update to two method test pattern
05/02/2017 - MF - Update test for new AOI parameter in the tool
07/28/2017 - CM - Refactor
==================================================
'''

import arcpy
import os
import unittest

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration
import DataDownload
import arcpyAssert

class CountIncidentsByLOCTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    ''' Test all tools and methods related to the Count Incidents by LOC tool
    in the Incident Analysis toolbox'''
   
    toolboxUnderTest = None # Set to Pro or ArcMap toolbox at runtime
    toolboxUnderTestAlias = 'iaTools'

    incidentScratchGDB = None    
     
    inputPointsFeatures = None
    inputLinesFeatures = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print(".....CountIncidentsByLOCTestCase.setUp")  

        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''

        self.toolboxUnderTest = Configuration.incidentToolboxPath + Configuration.GetToolboxSuffix()

        UnitTestUtilities.checkArcPy()
        
        DataDownload.runDataDownload(Configuration.incidentAnalysisDataPath, Configuration.incidentInputGDB, Configuration.incidentURL)
        if (self.incidentScratchGDB == None) or (not arcpy.Exists(self.incidentScratchGDB)):
            self.incidentScratchGDB = UnitTestUtilities.createScratch(Configuration.incidentAnalysisDataPath)
        
        # set up inputs    
        self.inputPointsFeatures = os.path.join(Configuration.incidentInputGDB, "Incidents")
        self.inputLinesFeatures = os.path.join(Configuration.incidentInputGDB, "Roads")
        self.inputAOIFeatures = os.path.join(Configuration.incidentInputGDB, "Districts")
        self.resultCompareFeatures0001 = os.path.join(Configuration.incidentResultGDB, "resultsCountIncidentsByLOC_0001")

        UnitTestUtilities.checkFilePaths([Configuration.incidentAnalysisDataPath])

        UnitTestUtilities.checkGeoObjects([Configuration.incidentInputGDB, \
                                           self.incidentScratchGDB, \
                                           self.toolboxUnderTest, \
                                           self.inputPointsFeatures, \
                                           self.inputLinesFeatures,  \
                                           self.inputAOIFeatures,  \
                                           self.resultCompareFeatures0001])
            
    def tearDown(self):
        if Configuration.DEBUG == True: print(".....CountIncidentsByLOCTestCase.tearDown")
        UnitTestUtilities.deleteScratch(self.incidentScratchGDB)
                
    def test_count_incidents(self):
        '''test_count_incidents'''
        if Configuration.DEBUG == True: print(".....CountIncidentsByLOCTestCase.test_count_incidents")

        arcpy.ImportToolbox(self.toolboxUnderTest, self.toolboxUnderTestAlias)

        outputCountFeatures = os.path.join(self.incidentScratchGDB, "outputCount")
        runToolMsg = "Running tool (Count Incidents By LOC)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        arcpy.CountIncidentsByLOC_iaTools(self.inputPointsFeatures,
                                          self.inputLinesFeatures,
                                          self.inputAOIFeatures,
                                          outputCountFeatures,
                                          "50 Meters")
        self.assertFeatureClassEqual(self.resultCompareFeatures0001, outputCountFeatures, "OBJECTID")

if __name__ == "__main__":
    unittest.main()