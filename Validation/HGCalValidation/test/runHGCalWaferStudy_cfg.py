import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('PROD',eras.Phase2C4)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load('Configuration.Geometry.GeometryExtended2023D28_cff')
process.load('Configuration.Geometry.GeometryExtended2023D28Reco_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Validation.HGCalValidation.hgcalWaferStudy_cfi')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['phase2_realistic']

if hasattr(process,'MessageLogger'):
    process.MessageLogger.categories.append('HGCalValidation')

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        'file:step2.root',
        )
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('hgcWafer.root'),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

process.raw2digi_step = cms.Path(process.RawToDigi)
process.analysis_step = cms.Path(process.hgcalWaferStudy)
process.hgcalWaferStudy.verbosity = 0
process.hgcalWaferStudy.nBinHit   = 100
process.hgcalWaferStudy.nBinDig   = 100
process.hgcalWaferStudy.layerMinSim = cms.untracked.vint32(1,1)
process.hgcalWaferStudy.layerMaxSim = cms.untracked.vint32(10,10)
process.hgcalWaferStudy.layerMinDig = cms.untracked.vint32(1,1)
process.hgcalWaferStudy.layerMaxDig = cms.untracked.vint32(10,10)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.analysis_step)
