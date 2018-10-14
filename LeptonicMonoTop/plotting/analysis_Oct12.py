#!/usr/bin/env python 

from os import system,getenv
from sys import argv
import argparse,sys 


### SET GLOBAL VARIABLES ###
baseDir="/uscms_data/d3/fdolek/panda/80X-v1.6/lep_monotop/flat/"
dataDir=baseDir
parser = argparse.ArgumentParser(description='plot stuff')
parser.add_argument('--outdir',metavar='outdir',type=str,default='.')
parser.add_argument('--cut',metavar='cut',type=str,default='1==1')
parser.add_argument('--region',metavar='region',type=str,default=None)
parser.add_argument('--tt',metavar='tt',type=str,default='')
parser.add_argument('--bdtcut',type=float,default=None)
parser.add_argument('--masscut',type=float,default=None)
args = parser.parse_args() 
lumi = 35800.
blind=True
region = args.region 
sname = argv[0]

argv=[]
import ROOT as root
root.gROOT.SetBatch()
from PandaCore.Tools.Misc import *
import PandaCore.Tools.Functions
from PandaCore.Drawers.plot_utility import *
import PandaAnalysis.LeptonicMonoTop.LeptonicMonotopSelection as sel
#import PandaAnalysis.MonoX.MonoXSelection as sel                                                                                                                                                         
from PandaCore.Drawers.plot_utility import *

#reload(sys.modules['plot_utility'])

### SET GLOBAL VARIABLES ### 
#########     baseDir = getenv('PANDA_FLATDIR') 
#dataDir = baseDir#.replace('0_4', '0_4_egfix')

### DEFINE REGIONS ###
print "PLOTTER: input directory is:", baseDir
cut = tAND(sel.cuts[args.region],args.cut)
if args.bdtcut:
    cut = tAND(cut,'top_ecf_bdt>%f'%args.bdtcut)
if args.masscut:
    cut = tAND(cut,'fj1MSD>%f'%args.masscut)


### LOAD PLOTTING UTILITY ###
plot = PlotUtility()
plot.Stack(True)
plot.Ratio(True)
plot.FixRatio(0.4)
if 'qcd' in region:
    plot.FixRatio(1)
plot.SetTDRStyle()
plot.InitLegend()
plot.cut = cut
plot.DrawMCErrors(True)
plot.AddCMSLabel()
plot.SetEvtNum("eventNumber")
plot.SetLumi(lumi/1000)
plot.AddLumiLabel(True)
plot.do_overflow = True
plot.do_underflow = True


weight = sel.weights[region]%lumi
plot.mc_weight = weight

if args.bdtcut:
    plot.AddPlotLabel('BDT > %.2f'%args.bdtcut,.18,.7,False,42,.04)
if args.masscut:
    plot.AddPlotLabel('%i < m_{SD} < 210 GeV'%(int(args.masscut)),.18,.7,False,42,.04)

PInfo('cut',plot.cut)
PInfo('weight',plot.mc_weight)

#plot.add_systematic('QCD scale','scaleUp','scaleDown',root.kRed+2)
#plot.add_systematic('PDF','pdfUp','pdfDown',root.kBlue+2)

    ### DEFINE PROCESSES ###

zjets         = Process('Z+jets',root.kZjets,None,root.kCyan-9)
wjets         = Process('W+jets',root.kWjets,None,root.kGreen-10)
#diboson       = Process('Diboson',root.kDiboson,None,root.kYellow-9)
#ttbar         = Process('t#bar{t}',root.kTTbar,None,root.kOrange-4) 
#ttbar1l       = Process('t#bar{t} 1l',root.kTTbar1l,None,root.kOrange-3)
#ttbar2l       = Process('t#bar{t} 2l',root.kTTbar2l,None,root.kOrange-5)
#ttg           = Process('t#bar{t}#gamma',root.kTTbar)
#singletop     = Process('Single t',root.kST,None,root.kRed-9)
#singletopg    = Process('t#gamma',root.kST)
#qcd           = Process("QCD",root.kQCD,None,root.kMagenta-10)
#gjets         = Process('#gamma+jets',root.kGjets)
data          = Process("Data",root.kData)
signal        = Process('m_{V}=1.75 TeV, m_{#chi}=1 GeV',root.kSignal)
#processes = [qcd,diboson,singletop,ttbar,wewk,zewk,wjets,zjets]
#processes = [qcd,diboson,singletop,wjets,ttbar,zjets]
processes = [wjets, zjets]
#if 'qcd' in region:
#    processes = [wjets, zjets]

### ASSIGN FILES TO PROCESSES ###
if 'signal' in region or 'qcd' in region:
    #zjets.add_file(baseDir+'ZtoNuNu.root')
    signal.add_file(baseDir+'Vector_MonoTop_Leptonic_Mphi_1750_Mchi_1.root') 
else:
    zjets.add_file(baseDir+'ZJets.root')
    wjets.add_file(baseDir+'WJets.root')
  #diboson.add_file(baseDir+'Diboson.root')
  #ttbar.add_file(baseDir+'TTbar%s.root'%(args.tt));
  #singletop.add_file(baseDir+'SingleTop.root')
#ttg.add_file(baseDir+'TTbar_Photon.root');
#singletopg.add_file(baseDir+'SingleTop_tG.root')
#if 'pho' in region:
    #processes = [qcd,singletopg,ttg,gjets]
    #processes = [qcd,gjets]
    #gjets.add_file(baseDir+'GJets.root')
    #qcd.add_file(baseDir+'SinglePhoton.root')
    #qcd.additional_cut = sel.triggers['pho']
    #qcd.use_common_weight = False
    #qcd.additional_weight = 'sf_phoPurity'
#else:
    #qcd.add_file(baseDir+'QCD.root')


if any([x in region for x in ['singlemuonw','singleelectronw']]):
    processes = [zjets, wjets] 
if any([x in region for x in ['singlemuontop','singleelectrontop']]):
    processes = [zjets, wjets]
#if any([x in region for x in ['signal','muon','qcd']]):
    #data.additional_cut = sel.triggers['met']
    #data.add_file(dataDir+'MET.root') 
    #lep='#mu'
elif 'electron' in region:
    if 'di' in region:
	 data.additional_cut = tOR(sel.triggers['ele']) 
        #data.additional_cut = tOR(sel.triggers['ele'],sel.triggers['pho'])
    else:
        data.additional_cut = sel.triggers['ele']
    data.add_file(dataDir+'SingleElectron.root')
    lep='e'
#elif region=='photon':
#    data.additional_cut = sel.triggers['pho']
#    data.add_file(dataDir+'SinglePhoton.root')
#elif region=='ZmmCR':
#    data.additional_cut = sel.triggers['met']
#    print dataDir+'MET.root'
#    data.add_file(dataDir+'MET.root')
#    lep='#mu' 

processes.append(data)
for p in processes:
    plot.add_process(p)

recoilBins = [250,280,310,350,400,450,600,1000]
nRecoilBins = len(recoilBins)-1

    ### CHOOSE DISTRIBUTIONS, LABELS ###
if 'wjets' in region or 'zjets' in region:
#if 'signal' in region or 'qcd' in region: 
    recoil=VDistribution("pfmet",recoilBins,"PF MET [GeV]","Events/GeV")

#elif any([x in region for x in ['singlemuonw','singleelectronw','singlemuontop','singleelectrontop','singlemuon','singleelectron']]):
#    recoil=VDistribution("pfUWmag",recoilBins,"PF U(%s) [GeV]"%(lep),"Events/GeV")
#    plot.add_distribution(FDistribution('looseLep1Pt',0,1000,20,'Leading %s p_{T} [GeV]'%lep,'Events/40 GeV'))
#    plot.add_distribution(FDistribution('looseLep1Eta',-2.5,2.5,20,'Leading %s #eta'%lep,'Events/bin'))
#elif any([x in region for x in ['dielectron','dimuon']]):
#    recoil=VDistribution("pfUZmag",recoilBins,"PF U(%s%s) [GeV]"%(lep,lep),"Events/GeV")
#    plot.add_distribution(FDistribution('diLepMass',60,120,20,'m_{ll} [GeV]','Events/3 GeV'))
#    plot.add_distribution(FDistribution('looseLep1Pt',0,1000,20,'Leading %s p_{T} [GeV]'%lep,'Events/40 GeV'))
#    plot.add_distribution(FDistribution('looseLep1Eta',-2.5,2.5,20,'Leading %s #eta'%lep,'Events/bin'))
#    plot.add_distribution(FDistribution('looseLep2Pt',0,1000,20,'Subleading %s p_{T} [GeV]'%lep,'Events/40 GeV'))
#    plot.add_distribution(FDistribution('looseLep2Eta',-2.5,2.5,20,'Subleading %s #eta'%lep,'Events/bin'))
#elif regio
#n=='photon':
#    recoil=VDistribution("pfUAmag",recoilBins,"PF U(#gamma) [GeV]","Events/GeV")
#    plot.add_distribution(FDistribution('loosePho1Pt',0,1000,20,'Leading #gamma p_{T} [GeV]','Events/40 GeV'))
#    plot.add_distribution(FDistribution('loosePho1Eta',-2.5,2.5,20,'Leading #gamma #eta','Events/bin'))
#elif region=='ZmmCR':
#    recoil=VDistribution("pfUZmag",recoilBins,"PF U(%s%s) [GeV]"%(lep,lep),"Events/GeV")
#    plot.add_distribution(FDistribution('diLepMass',60,120,20,'m_{ll} [GeV]','Events/3 GeV'))



### DRAW AND CATALOGUE ###
if args.bdtcut:
    region += ('_bdt%.2f'%(args.bdtcut)).replace('.','p').replace('-','m')
if args.masscut:
    region += ('_mass%i'%(int(args.masscut)))
plot.draw_all(args.outdir+'/'+region+'_')
