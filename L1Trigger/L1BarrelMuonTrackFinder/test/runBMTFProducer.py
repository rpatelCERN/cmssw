# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
process = cms.Process("L1TMuonEmulation")
import os
import sys
import commands

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(50)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.source = cms.Source(
    'PoolSource',
#    fileNames = cms.untracked.vstring('file:./omtf_input_test.root')
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/g/gflouris/public/SingleMuPt5To140_Eta01_Flat_NoAntiparticle.root')

    )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500))

# PostLS1 geometry used
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
############################
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')


#process.MicroGMTInputProducer = cms.EDProducer("l1t::MicroGMTInputProducerFromGen",
#)

#process.load('L1Trigger.L1EndcapMuonTrackFinder.L1TMuonTriggerPrimitiveProducer_cfi')

#process.load("L1Trigger.L1TMuon.microgmtemulator_cfi")

#process.microGMTEmulator.barrelTFInput = cms.InputTag("mtfEmulator", "BMTF")




process.load('L1Trigger.L1BarrelMuonTrackFinder.bmtfDigis_cfi')


####BMTF Emulator
process.bmtfEmulator = cms.EDProducer("BMTrackFinder",
    DTDigi_Source = cms.InputTag("simDtTriggerPrimitiveDigis"),
    CSCStub_Source = cms.InputTag("none"),
    Debug = cms.untracked.int32(0)

)


process.L1TMuonSeq = cms.Sequence( #process.L1TMuonTriggerPrimitives +
                                   #process.emtfEmulator +
                                   process.bmtfEmulator#+ 
				   #process.omtfEmulator 
                                   #process.MicroGMTInputProducer +
                                   #process.microGMTEmulator
                                   #  +
                                   # process.emtfEmulator + 
                                   # process.bmtfEmulator +
                                   # process.caloEmulator
)

process.L1TMuonPath = cms.Path(process.L1TMuonSeq)


process.out = cms.OutputModule("PoolOutputModule", 
   fileName = cms.untracked.string("l1tbmtf_test.root"),
                               )

process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.L1TMuonPath)
process.schedule.extend([process.output_step])
