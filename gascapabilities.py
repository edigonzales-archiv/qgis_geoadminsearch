# -*- coding: utf-8 -*-

class GasCapabilities():
    def __init__(self):
        pass
    
    @staticmethod
    def isSearchable(layerName):
        searchableLayers = [
            'ch.swisstopo.verschiebungsvektoren-tsp2',
            'ch.swisstopo.verschiebungsvektoren-tsp1',
            'ch.swisstopo.swissboundaries3d-kanton-flaeche.fill',
            'ch.swisstopo.lubis-luftbilder_infrarot',
            'ch.astra.strassenverkehrszaehlung_messstellen-uebergeordnet',
            'ch.bafu.hydrologie-wassertemperaturmessstationen',
            'ch.swisstopo.lubis-bildstreifen',
            'ch.bazl.sicherheitszonenplan',
            'ch.swisstopo.lubis-luftbilder-dritte-kantone',
            'ch.astra.strassenverkehrszaehlung_messstellen-regional_lokal',
            'ch.swisstopo.fixpunkte-hfp1',
            'ch.babs.kulturgueter',
            'ch.swisstopo.lubis-luftbilder_schwarzweiss',
            'ch.bakom.versorgungsgebiet-tv',
            'ch.swisstopo.geologie-gravimetrischer_atlas.metadata',
            'ch.bafu.hydrologie-gewaesserzustandsmessstationen',
            'ch.astra.ivs-nat',
            'ch.astra.ivs-reg_loc',
            'ch.bav.sachplan-infrastruktur-schiene_kraft',
            'ch.swisstopo.lubis-luftbilder_farbe',
            'ch.bfs.gebaeude_wohnungs_register',
            'ch.swisstopo.swissboundaries3d-bezirk-flaeche.fill',
            'ch.swisstopo.fixpunkte-lfp1',
            'ch.swisstopo.fixpunkte-lfp2',
            'ch.swisstopo.lubis-luftbilder-dritte-firmen',
            'ch.swisstopo.vec200-names-namedlocation',
            'ch.swisstopo-vd.ortschaftenverzeichnis_plz',
            'ch.astra.ivs-nat-verlaeufe',
            'ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill',
            'ch.bakom.versorgungsgebiet-ukw',
            'ch.bakom.radio-fernsehsender',
            'ch.swisstopo.fixpunkte-hfp2']     
        
        if layerName in searchableLayers:
            return True
        else:
            return False

