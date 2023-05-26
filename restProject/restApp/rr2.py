from .models import *
from rest_framework.response import Response
import pandas as pd
import numpy as np
from django.db.models import Q


def RRFunctionsNonLevee(inputs):
    # Base Rate
    baserate = baseRateMultipliers.objects.filter(
        levee=inputs['Levee'], region=inputs['State'], singleFamilyHomeIndicator=inputs['Single family home indicator'], bi=inputs['Barrier island indicator']).all()

    item1 = "Base Rate (per $1000 of Coverage Value)"
    segment = baserate.values()[0]['segment']
    ifBuilding = baserate.values()[0]['ifBuilding']
    ifContents = baserate.values()[0]['ifContents']
    ssBuilding = baserate.values()[0]['ssBuilding']
    ssContents = baserate.values()[0]['ssContents']
    tsuBuilding = baserate.values()[0]['tsuBuilding']
    tsuContents = baserate.values()[0]['tsuContents']
    glBuilding = baserate.values()[0]['glBuilding']
    glContents = baserate.values()[0]['glContents']
    ceBuilding = baserate.values()[0]['ceBuilding']
    ceContents = baserate.values()[0]['ceContents']
    allPerils = ''

    baserateResults_dict = {"items": item1, "Segment": segment,
                            "ifBuilding": ifBuilding, "ifContents": ifContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}
    # print("baserate Results  : ", baserateResults_dict)

    baseRateResult = riskrating2results(items=item1,
                                        inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                        stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                        tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                        greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                        coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                        )
    baseRateResult.save()

    # Distance To River
    segmentfromBaserate = baserate.values()[0]['segment']

    disttoriver = distToRiverMultipliers.objects.filter(
        levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate)).all()
    dtrMeters = disttoriver.values_list("dtr_meters", flat=True)
    dtrMeters = list(dtrMeters)
    ifvalue = disttoriver.values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    if inputs['DTR'] == 'N/A':
        B = -9999.0  # np.nan
    else:
        B = np.interp([inputs['DTR']], dtrMeters,
                      ifvalue)

    item2 = "Distance to River"
    ifBuilding = round(float(B), 4)
    ifContents = round(float(B), 4)
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    distToRiverResults_dict = {"items": item2,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("distToRiver Results  : ", distToRiverResults_dict)
    distToRiverResult = riskrating2results(items=item2,
                                           inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    distToRiverResult.save()

    # Elevation Relative To River
    segmentfromBaserate = segment

    elevRiver = elevRelToRiver.objects.filter(
        levee=inputs['Levee'], segment=segmentfromBaserate, riverClass='Class '+str(inputs['River class'])).all()

    err_feet = elevRiver.values_list("err_feet", flat=True)
    err_feet = list(err_feet)
    ifvalue = elevRiver.values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    if inputs['ERR'] == 'N/A':
        C = -9999.0  # np.nan
    else:
        C = np.interp([inputs['ERR']], err_feet,
                      ifvalue)

    item3 = "Elevation Relative to River by River Class"
    ifBuilding = round(float(C), 4)
    ifContents = round(float(C), 4)
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    elevRelToRiverResults_dict = {"items": item3,
                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                  "glBuilding": glBuilding, "glContents": glContents,
                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                  "allPerils": allPerils}

    # print("elevRelToRiverResults_dict  : ", elevRelToRiverResults_dict)
    elevRelToRiverResults = riskrating2results(items=item3,
                                               inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    elevRelToRiverResults.save()

    # Drainage Area
    segmentfromBaserate = baserate.values()[0]['segment']

    drainArea = drainageAreaMultipliers.objects.filter(
        levee=inputs['Levee'], segment=segmentfromBaserate).all()

    da_km2 = drainArea.values_list("da_km2", flat=True)
    da_km2 = list(da_km2)
    ifvalue = drainArea.values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    D = np.interp([inputs['DA']], da_km2, ifvalue)

    item4 = "Drainage Area"
    ifBuilding = round(float(D), 4)
    ifContents = round(float(D), 4)
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    drainageAreaResults_dict = {"items": item4,
                                "ifBuilding": ifBuilding, "ifContents": ifContents,
                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                "glBuilding": glBuilding, "glContents": glContents,
                                "ceBuilding": ceBuilding, "ceContents": ceContents,
                                "allPerils": allPerils}

    # print("drainageAreaResults_dict  : ", drainageAreaResults_dict)
    drainageAreaResults = riskrating2results(items=item4,
                                             inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    drainageAreaResults.save()

    # Strucral Relative Elevation
    strucRelElv = structuralRelElevation.objects.filter(
        levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate)).all()

    sre_feet = strucRelElv .values_list("sre_feet", flat=True)
    sre_feet = list(sre_feet)
    ifvalue = strucRelElv .values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    E = np.interp([inputs['SRE']], sre_feet, ifvalue)

    item5 = "Structural Relative Elevation"
    ifBuilding = round(float(E), 4)
    ifContents = round(float(E), 4)
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    strucRelElvResults_dict = {"items": item5,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("strucRelElvResults_dict  : ", strucRelElvResults_dict)
    strucRelElvResults = riskrating2results(items=item5,
                                            inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    strucRelElvResults.save()

    # Distance To Coast
    distToCoast = distToCoastMultipliers.objects.filter(
        levee=inputs['Levee']).all()

    dtc_meters = distToCoast.filter(
        ~Q(ce=-9999.0)).values_list("dtc_meters", flat=True)
    dtc_meters = list(dtc_meters)
    ce = distToCoast.filter(
        ~Q(ce=-9999.0)).values_list("ce", flat=True)
    ce = list(ce)

    if inputs['DTC'] == 'N/A':
        coast = -9999.0  # np.nan
    else:
        coast = np.interp([inputs['DTC']], dtc_meters, ce)

    if segmentfromBaserate != 3 and segmentfromBaserate != 4 and inputs['DTC'] != 'N/A':
        dtc_others = distToCoastMultipliers.objects.filter(
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), bi=inputs['Barrier island indicator']).all()
        dtc_meters_ss = dtc_others.filter(
            ~Q(ss=-9999.0)).values_list("dtc_meters", flat=True)
        dtc_meters_ss = list(dtc_meters_ss)
        dtc_meters_tsu = dtc_others.filter(
            ~Q(tsu=-9999.0)).values_list("dtc_meters", flat=True)
        dtc_meters_tsu = list(dtc_meters_tsu)
        ss = dtc_others.filter(
            ~Q(ss=-9999.0)).values_list("ss", flat=True)
        ss = list(ss)
        tsu = dtc_others.filter(
            ~Q(tsu=-9999.0)).values_list("tsu", flat=True)
        tsu = list(tsu)

        storm = np.interp([inputs['DTC']], dtc_meters_ss, ss)
        tsunami = np.interp([inputs['DTC']], dtc_meters_tsu, tsu)
    else:
        storm = -9999.0  # np.nan
        tsunami = -9999.0  # np.nan

    item6 = "Distance to Coast"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = round(float(storm), 4)
    ssContents = round(float(storm), 4)
    tsuBuilding = round(float(tsunami), 4)
    tsuContents = round(float(tsunami), 4)
    glBuilding = ''
    glContents = ''
    ceBuilding = round(float(coast), 4)
    ceContents = round(float(coast), 4)
    allPerils = ''

    distToCoastResults_dict = {"items": item6,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("distToCoastResults_dict  : ", distToCoastResults_dict)
    distToCoastResults = riskrating2results(items=item6,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                            coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents)
    distToCoastResults.save()

    # Distance To Ocean
    if segmentfromBaserate != 3 and segmentfromBaserate != 4 and inputs['DTO'] != 'N/A':
        dto = distToOceanMultipliers.objects.filter(
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), bi=inputs['Barrier island indicator']).all()
        dto_ss = dto.filter(
            ~Q(ss=-9999.0)).values_list("dto_meters", flat=True)
        dto_ss = list(dto_ss)
        dto_tsu = dto.filter(
            ~Q(tsu=-9999.0)).values_list("dto_meters", flat=True)
        dto_tsu = list(dto_tsu)
        ss = dto.filter(
            ~Q(ss=-9999.0)).values_list("ss", flat=True)
        ss = list(ss)
        tsu = dto.filter(
            ~Q(tsu=-9999.0)).values_list("tsu", flat=True)
        tsu = list(tsu)

        storm = np.interp([inputs['DTO']], dto_ss, ss)
        tsunami = np.interp([inputs['DTO']], dto_tsu, tsu)
    else:
        storm = -9999.0  # np.nan
        tsunami = -9999.0  # np.nan

    item7 = "Distance to Ocean"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = round(float(storm), 4)
    ssContents = round(float(storm), 4)
    tsuBuilding = round(float(tsunami), 4)
    tsuContents = round(float(tsunami), 4)
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    distToOceanResults_dict = {"items": item7,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("distToOceanResults_dict  : ", distToOceanResults_dict)
    distToOceanResults = riskrating2results(items=item7,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents
                                            )
    distToOceanResults.save()

    # Elevation
    if segmentfromBaserate != 3 and segmentfromBaserate != 4:
        elev = elevation.objects.filter(
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), bi=inputs['Barrier island indicator']).all()
        elev_ss = elev.filter(
            ~Q(ss=-9999.0)).values_list("elevation_feet", flat=True)
        elev_ss = list(elev_ss)
        elev_tsu = elev.filter(
            ~Q(tsu=-9999.0)).values_list("elevation_feet", flat=True)
        elev_tsu = list(elev_tsu)
        ss = elev.filter(
            ~Q(ss=-9999.0)).values_list("ss", flat=True)
        ss = list(ss)
        tsu = elev.filter(
            ~Q(tsu=-9999.0)).values_list("tsu", flat=True)
        tsu = list(tsu)

        storm = np.interp([inputs['Elevation']], elev_ss, ss)
        tsunami = np.interp([inputs['Elevation']], elev_tsu, tsu)
    else:
        storm = -9999.0  # np.nan
        tsunami = -9999.0  # np.nan

    item8 = "Elevation"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = round(float(storm), 4)
    ssContents = round(float(storm), 4)
    tsuBuilding = round(float(tsunami), 4)
    tsuContents = round(float(tsunami), 4)
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    elevationResults_dict = {"items": item8,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("elevationResults_dict  : ", elevationResults_dict)
    elevationResults = riskrating2results(items=item8,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents
                                          )
    elevationResults.save()

    # Distance To Lake
    dist_lake = distToLakeMultipliers.objects.filter(
        levee=inputs['Levee']).all()

    if inputs['DTL'] == 'N/A':
        greatlakesbuilding = 0.525
        greatlakescontent = 0.525
    else:
        dtl_meters = dist_lake.filter(
            ~Q(gl=-9999.0)).values_list("dtl_meters", flat=True)
        dtl_meters = list(dtl_meters)
        gl = dist_lake.filter(
            ~Q(gl=-9999.0)).values_list("gl", flat=True)
        gl = list(gl)

        I = np.interp([inputs['DTL']], dtl_meters, gl)
        greatlakesbuilding = round(float(I), 4)
        greatlakescontent = round(float(I), 4)

    item9 = "Distance to Lake"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = greatlakesbuilding
    glContents = greatlakescontent
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    disttolakeResults_dict = {"items": item9,
                              "ifBuilding": ifBuilding, "ifContents": ifContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents,
                              "allPerils": allPerils}

    # print("disttolakeResults_dict  : ", disttolakeResults_dict)
    disttolakeResults = riskrating2results(items=item9,
                                           greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                           )
    disttolakeResults.save()

    # Elevation Relative To Lake
    elev_lake = elevRelToLake.objects.filter(
        levee=inputs['Levee']).all()

    if inputs['DTL'] == 'N/A':
        greatlakesbuilding = 0.004
        greatlakescontent = 0.004
    else:
        erl_feet = elev_lake.filter(
            ~Q(gl=-9999.0)).values_list("erl_feet", flat=True)
        erl_feet = list(erl_feet)
        gl = elev_lake.filter(
            ~Q(gl=-9999.0)).values_list("gl", flat=True)
        gl = list(gl)

        J = np.interp([inputs['ERL']], erl_feet, gl)
        greatlakesbuilding = round(float(J), 4)
        greatlakescontent = round(float(J), 4)

    item10 = "Elevation Relative to Lake"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = greatlakesbuilding
    glContents = greatlakescontent
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    elevationRelToLakeResults_dict = {"items": item10,
                                      "ifBuilding": ifBuilding, "ifContents": ifContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}

    # print("elevationRelToLakeResults_dict  : ", elevationRelToLakeResults_dict)
    elevationRelToLakeResults = riskrating2results(items=item10,
                                                   greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                   )
    elevationRelToLakeResults.save()

    # Territory
    # TSU
    territory_huc12_tsu = territory.objects.filter(
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), peril='Tsu').all()

    if territory_huc12_tsu.count() == 0:
        tsuBldg = 0.0
        tsuCont = 0.0
    else:
        territory_tsu = territory_huc12_tsu.filter(
            ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
        territory_tsu = list(territory_tsu)
        tsuBldg = round(territory_tsu[0], 4)
        tsuCont = round(territory_tsu[0], 4)

    # GL
    territory_huc12_gl = territory.objects.filter(
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), peril='GL').all()

    if territory_huc12_gl.count() == 0:
        glBldg = 0.0
        glCont = 0.0
    else:
        territory_gl = territory_huc12_gl.filter(
            ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
        territory_gl = list(territory_gl)
        glBldg = round(territory_gl[0], 4)
        glCont = round(territory_gl[0], 4)

    # IF
    territory_huc12_if = territory.objects.filter(
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), bi=inputs['Barrier island indicator'], peril='IF').all()

    territory_if = territory_huc12_if.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_if = list(territory_if)
    ifBldg = round(territory_if[0], 4)
    ifCont = round(territory_if[0], 4)

    # SS
    territory_huc12_ss = territory.objects.filter(
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), bi=inputs['Barrier island indicator'], peril='SS').all()

    territory_ss = territory_huc12_ss.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_ss = list(territory_ss)
    ssBldg = round(territory_ss[0], 4)
    ssCont = round(territory_ss[0], 4)

    item11 = "Territory (HUC12 & Barrier Island Indicator)"
    ifBuilding = ifBldg
    ifContents = ifCont
    ssBuilding = ssBldg
    ssContents = ssCont
    tsuBuilding = tsuBldg
    tsuContents = tsuCont
    glBuilding = glBldg
    glContents = glCont
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    territoryResults_dict = {"items": item11,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("territoryResults_dict  : ", territoryResults_dict)
    territoryResults = riskrating2results(items=item11,
                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                          )
    territoryResults.save()

    # Type Of Use
    typeuse = typeOfUSe.objects.filter(
        typeofuse=inputs['Type of Use']).all()

    typeuse_if = typeuse.values_list('flood', flat=True)
    typeuse_if = list(typeuse_if)
    typeuse_ss = typeuse.values_list('surge', flat=True)
    typeuse_ss = list(typeuse_ss)
    typeuse_tsu = typeuse.values_list('tsunami', flat=True)
    typeuse_tsu = list(typeuse_tsu)
    typeuse_gl = typeuse.values_list('lakes', flat=True)
    typeuse_gl = list(typeuse_gl)

    item12 = "Type of Use"
    ifBuilding = typeuse_if[0]
    ifContents = typeuse_if[0]
    ssBuilding = typeuse_ss[0]
    ssContents = typeuse_ss[0]
    tsuBuilding = typeuse_tsu[0]
    tsuContents = typeuse_tsu[0]
    glBuilding = typeuse_gl[0]
    glContents = typeuse_gl[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    typeOfUseResults_dict = {"items": item12,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("typeOfUseResults_dict  : ", typeOfUseResults_dict)
    typeOfUseResults = riskrating2results(items=item12,
                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                          )
    typeOfUseResults.save()

    # Floors Of Interest
    floorsOfInt = floorsOfInterest.objects.filter(
        homeIndicator=inputs['Single family home indicator'], ownerIndicator=inputs['Condo unit owner indicator'], interest=inputs['Floor of interest']).all()

    floorsOfInt_allexclCE = floorsOfInt.values_list('allExclCE', flat=True)
    floorsOfInt_allexclCE = list(floorsOfInt_allexclCE)

    item12 = "Floor of Interest"
    ifBuilding = floorsOfInt_allexclCE[0]
    ifContents = floorsOfInt_allexclCE[0]
    ssBuilding = floorsOfInt_allexclCE[0]
    ssContents = floorsOfInt_allexclCE[0]
    tsuBuilding = floorsOfInt_allexclCE[0]
    tsuContents = floorsOfInt_allexclCE[0]
    glBuilding = floorsOfInt_allexclCE[0]
    glContents = floorsOfInt_allexclCE[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    floorsOfIntResults_dict = {"items": item12,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("floorsOfIntResults_dict  : ", floorsOfIntResults_dict)
    floorsOfIntResults = riskrating2results(items=item12,
                                            inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                            greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                            )
    floorsOfIntResults.save()

    # Foundation type
    foundation = foundationType.objects.filter(
        foundationtypes=inputs['Foundation type']).all()

    foundation_allexclCE = foundation.values_list('allExclCE', flat=True)
    foundation_allexclCE = list(foundation_allexclCE)

    item13 = "Foundation Type"
    ifBuilding = foundation_allexclCE[0]
    ifContents = foundation_allexclCE[0]
    ssBuilding = foundation_allexclCE[0]
    ssContents = foundation_allexclCE[0]
    tsuBuilding = foundation_allexclCE[0]
    tsuContents = foundation_allexclCE[0]
    glBuilding = foundation_allexclCE[0]
    glContents = foundation_allexclCE[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    foundationResults_dict = {"items": item13,
                              "ifBuilding": ifBuilding, "ifContents": ifContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents,
                              "allPerils": allPerils}

    # print("foundationResults_dict  : ", foundationResults_dict)
    foundationResults = riskrating2results(items=item13,
                                           inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                           stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                           tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                           greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                           )
    foundationResults.save()

    # Height Design Vent
    First_floor_foundation_vent = firstFloorHeight.objects.all()

    fffvHeight = First_floor_foundation_vent.values_list(
        'height', flat=True)
    fffvHeight = list(fffvHeight)

    fffvOpenNoObsWFV = First_floor_foundation_vent.values_list(
        'openNoObstructionWFV', flat=True)
    fffvOpenNoObsWFV = list(fffvOpenNoObsWFV)
    fffvOpenNoObsWbyFV = First_floor_foundation_vent.values_list(
        'openNoObstructionWbyFV', flat=True)
    fffvOpenNoObsWbyFV = list(fffvOpenNoObsWbyFV)

    fffvOpenObsWFV = First_floor_foundation_vent.values_list(
        'openObstructionWFV', flat=True)
    fffvOpenObsWFV = list(fffvOpenObsWFV)
    fffvOpenObsWbyFV = First_floor_foundation_vent.values_list(
        'openObstructionWbyFV', flat=True)
    fffvOpenObsWbyFV = list(fffvOpenObsWbyFV)

    fffvClosedWallWFV = First_floor_foundation_vent.values_list(
        'closedWallWFV', flat=True)
    fffvClosedWallWFV = list(fffvClosedWallWFV)
    fffvClosedWallWbyFV = First_floor_foundation_vent.values_list(
        'closedWallWbyFV', flat=True)
    fffvClosedWallWbyFV = list(fffvClosedWallWbyFV)

    if inputs['Foundation design'] == "Open, No Obstruction":
        floodEventyesWFV = fffvOpenNoObsWFV
        floodEventnoWbyFV = fffvOpenNoObsWbyFV
    elif inputs['Foundation design'] == "Open, Obstruction":
        floodEventyesWFV = fffvOpenObsWFV
        floodEventnoWbyFV = fffvOpenObsWbyFV
    elif inputs['Foundation design'] == "Closed, Wall":
        floodEventyesWFV = fffvClosedWallWFV
        floodEventnoWbyFV = fffvClosedWallWbyFV

    # floodEventnoWbyFV = fffvOpenNoObsWbyFV  # testing purpose, to be excluded
    if inputs['Flood vents'] == "Yes":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventyesWFV)
    elif inputs['Flood vents'] == "No":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventnoWbyFV)
    print("fffvHeight = ")
    print(fffvHeight)
    print("floodEventnoWbyFV = ")
    print(floodEventnoWbyFV)
    print("First_floor_foundation_vent = ", P)

    P = round(float(P), 4)

    item14 = "First Floor Height by Foundation Design & Flood Vents"
    segment = ''
    ifBuilding = P
    ifContents = P
    ssBuilding = P
    ssContents = P
    tsuBuilding = P
    tsuContents = P
    glBuilding = P
    glContents = P
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    firstFloorHeightResults_dict = {"items": item14, "Segment": segment,
                                    "ifBuilding": ifBuilding, "ifContents": ifContents,
                                    "ssBuilding": ssBuilding, "ssContents": ssContents,
                                    "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                    "glBuilding": glBuilding, "glContents": glContents,
                                    "ceBuilding": ceBuilding, "ceContents": ceContents,
                                    "allPerils": allPerils}

    # print("firstFloorHeightResults_dict  : ", firstFloorHeightResults_dict)
    firstFloorHeightResults = riskrating2results(items=item14,
                                                 inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                 stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                 tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                 greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                 )
    firstFloorHeightResults.save()

    # ME Above First Floor
    me = MEAboveFirstFloor.objects.filter(
        machineryEquipmentAboveFirstFloor=inputs['M&E']).all()

    meCE = float(me.values()[0]['coastalErosion'])

    item15 = "M&E above First Floor"
    ifBuilding = meCE
    ifContents = meCE
    ssBuilding = meCE
    ssContents = meCE
    tsuBuilding = meCE
    tsuContents = meCE
    glBuilding = meCE
    glContents = meCE
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    meAbovefirstFloorResults_dict = {"items": item15,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("meAbovefirstFloorResults_dict  : ", meAbovefirstFloorResults_dict)
    meAbovefirstFloorResults = riskrating2results(items=item15,
                                                  inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                  stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                  tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                  greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                  )
    meAbovefirstFloorResults.save()

    # Coverage Value
    bldgValue = buildingValue.objects.all()
    contValue = contentsValue.objects.all()

    bldgValue_value = bldgValue.values_list('value', flat=True)
    bldgValue_value = list(bldgValue_value)
    bldgValue_allexclCE = bldgValue.values_list('allExclCE', flat=True)
    bldgValue_allexclCE = list(bldgValue_allexclCE)
    contValue_value = contValue.values_list('value', flat=True)
    contValue_value = list(contValue_value)
    contValue_allexclCE = contValue.values_list('allExclCE', flat=True)
    contValue_allexclCE = list(contValue_allexclCE)

    build = np.interp([inputs['Coverage A value']], bldgValue_value,
                      bldgValue_allexclCE)
    content = np.interp([inputs['Coverage C value']], contValue_value,
                        contValue_allexclCE)

    item16 = "Coverage Value Factor"
    ifBuilding = round(float(build), 4)
    ifContents = round(float(content), 4)
    ssBuilding = round(float(build), 4)
    ssContents = round(float(content), 4)
    tsuBuilding = round(float(build), 4)
    tsuContents = round(float(content), 4)
    glBuilding = round(float(build), 4)
    glContents = round(float(content), 4)
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    coverageValueFactorResults_dict = {"items": item16,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("coverageValueFactorResults_dict  : ", coverageValueFactorResults_dict)
    coverageValueFactorResults = riskrating2results(items=item16,
                                                    inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                    stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                    tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                    greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                    )
    coverageValueFactorResults.save()

    # Deductible & Limit to Coverage Value Ratio
    deductible_limit_coverage_A = deductibleLimitITVCovA.objects.all()
    deductible_limit_coverage_C = deductibleLimitITVCovC.objects.all()

    ratio_A = max(min((inputs['Coverage A deductible'] +
                  inputs['Coverage A limit']) / inputs['Coverage A value'], 1), 0)
    ratio_C = max(min((inputs['Coverage C deductible'] +
                  inputs['Coverage C limit']) / inputs['Coverage C value'], 1), 0)

    coverageValueRatioLimitA = deductible_limit_coverage_A.values_list(
        'coverageValueRatio', flat=True)
    coverageValueRatioLimitA = list(coverageValueRatioLimitA)
    coverageValueRatioLimitC = deductible_limit_coverage_C.values_list(
        'coverageValueRatio', flat=True)
    coverageValueRatioLimitC = list(coverageValueRatioLimitC)

    inlandFloodLimitA = deductible_limit_coverage_A.values_list(
        'inlandFlood', flat=True)
    inlandFloodLimitA = list(inlandFloodLimitA)
    inlandFloodLimitC = deductible_limit_coverage_C.values_list(
        'inlandFlood', flat=True)
    inlandFloodLimitC = list(inlandFloodLimitC)

    ssTsuGlCeLimitA = deductible_limit_coverage_A.values_list(
        'SSTsunamiGreatLakesCoastalErosion', flat=True)
    ssTsuGlCeLimitA = list(ssTsuGlCeLimitA)
    ssTsuGlCeLimitC = deductible_limit_coverage_C.values_list(
        'SSTsunamiGreatLakesCoastalErosion', flat=True)
    ssTsuGlCeLimitC = list(ssTsuGlCeLimitC)

    S_build1_limit = np.interp(
        [ratio_A], coverageValueRatioLimitA, inlandFloodLimitA)
    S_build2_limit = np.interp(
        [ratio_A], coverageValueRatioLimitA, ssTsuGlCeLimitA)
    S_cont1_limit = np.interp(
        [ratio_C], coverageValueRatioLimitC, inlandFloodLimitC)
    S_cont2_limit = np.interp(
        [ratio_C], coverageValueRatioLimitC, ssTsuGlCeLimitC)

    item17 = "Deductible & Limit to Coverage Value Ratio"
    ifBuilding = round(float(S_build1_limit), 4)
    ifContents = round(float(S_cont1_limit), 4)
    ssBuilding = round(float(S_build2_limit), 4)
    ssContents = round(float(S_cont2_limit), 4)
    tsuBuilding = round(float(S_build2_limit), 4)
    tsuContents = round(float(S_cont2_limit), 4)
    glBuilding = round(float(S_build2_limit), 4)
    glContents = round(float(S_cont2_limit), 4)
    ceBuilding = round(float(S_build2_limit), 4)
    ceContents = round(float(S_cont2_limit), 4)
    allPerils = ''

    deductibleLimittoCoverageValueResults_dict = {"items": item17, "Segment": segment,
                                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                  "glBuilding": glBuilding, "glContents": glContents,
                                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                  "allPerils": allPerils}

    # print("deductibleLimittoCoverageValueResults_dict  : ", deductibleLimittoCoverageValueResults_dict)
    deductibleLimittoCoverageValueResults = riskrating2results(items=item17,
                                                               inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                               coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                               )
    deductibleLimittoCoverageValueResults.save()

    # Deductible to Coverage Value Ratio
    deductible_coverage_A = deductibleITVCovA.objects.all()
    deductible_coverage_C = deductibleITVCovC.objects.all()

    ratio_A = max(
        min((inputs['Coverage A deductible']) / inputs['Coverage A value'], 1), 0)
    ratio_C = max(
        min((inputs['Coverage C deductible']) / inputs['Coverage C value'], 1), 0)

    coverageValueRatioA = deductible_coverage_A.values_list(
        'coverageValueRatio', flat=True)
    coverageValueRatioA = list(coverageValueRatioA)
    coverageValueRatioC = deductible_coverage_C.values_list(
        'coverageValueRatio', flat=True)
    coverageValueRatioC = list(coverageValueRatioC)

    inlandFloodA = deductible_coverage_A.values_list(
        'inlandFlood', flat=True)
    inlandFloodA = list(inlandFloodA)
    inlandFloodC = deductible_coverage_C.values_list(
        'inlandFlood', flat=True)
    inlandFloodC = list(inlandFloodC)

    ssTsuGlCeA = deductible_coverage_A.values_list(
        'SSTsunamiGreatLakesCoastalErosion', flat=True)
    ssTsuGlCeA = list(ssTsuGlCeA)
    ssTsuGlCeC = deductible_coverage_C.values_list(
        'SSTsunamiGreatLakesCoastalErosion', flat=True)
    ssTsuGlCeC = list(ssTsuGlCeC)

    S_build1 = np.interp([ratio_A], coverageValueRatioA, inlandFloodA)
    S_build2 = np.interp([ratio_A], coverageValueRatioA, ssTsuGlCeA)
    S_cont1 = np.interp([ratio_C], coverageValueRatioC, inlandFloodC)
    S_cont2 = np.interp([ratio_C], coverageValueRatioC, ssTsuGlCeC)

    item18 = "Deductible to Coverage Value Ratio"
    ifBuilding = round(float(S_build1), 4)
    ifContents = round(float(S_cont1), 4)
    ssBuilding = round(float(S_build2), 4)
    ssContents = round(float(S_cont2), 4)
    tsuBuilding = round(float(S_build2), 4)
    tsuContents = round(float(S_cont2), 4)
    glBuilding = round(float(S_build2), 4)
    glContents = round(float(S_cont2), 4)
    ceBuilding = round(float(S_build2), 4)
    ceContents = round(float(S_cont2), 4)
    allPerils = ''

    deductibletoCoverageValueResults_dict = {"items": item18,
                                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                             "glBuilding": glBuilding, "glContents": glContents,
                                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                                             "allPerils": allPerils}

    # print("deductibletoCoverageValueResults_dict  : ", deductibletoCoverageValueResults_dict)
    deductibletoCoverageValueResults = riskrating2results(items=item18,
                                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                          coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                          )
    deductibletoCoverageValueResults.save()

    # Initial Deductible & ITV
    item19 = "Initial Deductible & ITV"
    S_build1int = round(float(S_build1_limit-S_build1), 4)
    S_cont1int = round(float(S_cont1_limit-S_cont1), 4)
    S_build2int = round(float(S_build2_limit-S_build2), 4)
    S_cont2int = round(float(S_cont2_limit-S_cont2), 4)

    ifBuilding = S_build1int
    ifContents = S_cont1int
    ssBuilding = S_build2int
    ssContents = S_cont2int
    tsuBuilding = S_build2int
    tsuContents = S_cont2int
    glBuilding = S_build2int
    glContents = S_cont2int
    ceBuilding = S_build2int
    ceContents = S_cont2int
    allPerils = ''

    initialDeductibleITVResults_dict = {"items": item19, "Segment": segment,
                                        "ifBuilding": ifBuilding, "ifContents": ifContents,
                                        "ssBuilding": ssBuilding, "ssContents": ssContents,
                                        "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                        "glBuilding": glBuilding, "glContents": glContents,
                                        "ceBuilding": ceBuilding, "ceContents": ceContents,
                                        "allPerils": allPerils}

    # print("initialDeductibleITVResults_dict  : ", initialDeductibleITVResults_dict)
    initialDeductibleITVResults = riskrating2results(items=item19,
                                                     inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                     stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                     tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                     greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                     coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                     )
    initialDeductibleITVResults.save()

    # Final Deductible & ITV
    item20 = "Final Deductible & ITV"
    segment = ''
    if inputs['Coverage A limit'] == 0:
        ifBuilding = 0
        ssBuilding = 0
        tsuBuilding = 0
        glBuilding = 0
        ceBuilding = 0
    else:
        ifBuilding = max(0.001, S_build1int)
        ssBuilding = max(0.001, S_build2int)
        tsuBuilding = max(0.001, S_build2int)
        glBuilding = max(0.001, S_build2int)
        ceBuilding = max(0.001, S_build2int)

    if inputs['Coverage A limit'] == 0:
        ifContents = 0
        ssContents = 0
        tsuContents = 0
        glContents = 0
        ceContents = 0
    else:
        ifContents = max(0.001, S_cont1int)
        ssContents = max(0.001, S_cont2int)
        tsuContents = max(0.001, S_cont2int)
        glContents = max(0.001, S_cont2int)
        ceContents = max(0.001, S_cont2int)
    allPerils = ''

    finalDeductibleITVResults_dict = {"items": item20, "Segment": segment,
                                      "ifBuilding": ifBuilding, "ifContents": ifContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}
    # print("finalDeductibleITVResults_dict  : ", finalDeductibleITVResults_dict)
    finalDeductibleITVResults = riskrating2results(items=item20,
                                                   inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                   stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                   tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                   greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                   coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                   )
    finalDeductibleITVResults.save()

    # Concentration Risk
    conc_risk_mapping = concentrationRiskMapping.objects.filter(
        state=inputs['State (Long)'], county=inputs['County']).all()
    print("conc_risk_mapping = ", conc_risk_mapping)
    msa = conc_risk_mapping.values()[0]['concentrationRiskTerritory']

    conc_risk = concentrationRisk.objects.filter(
        MSA=msa).all()

    item20 = "Concentration Risk"
    segment = ''

    ifBuilding = conc_risk.values()[0]['flood']
    ifContents = conc_risk.values()[0]['flood']
    ssBuilding = conc_risk.values()[0]['surge']
    ssContents = conc_risk.values()[0]['surge']
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    concRiskResults_dict = {"items": item20, "Segment": segment,
                            "ifBuilding": ifBuilding, "ifContents": ifContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}

    # print("concRiskResults_dict  : ", concRiskResults_dict)
    concRiskResults = riskrating2results(items=item20,
                                         inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                         stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                         )
    concRiskResults.save()

    # CRS Discount Percentage
    CRSDiscountPercentage = float(inputs['CRS discount']/100)
    item21 = "CRS Discount Percentage"
    ifBuilding = CRSDiscountPercentage
    ifContents = CRSDiscountPercentage
    ssBuilding = CRSDiscountPercentage
    ssContents = CRSDiscountPercentage
    tsuBuilding = CRSDiscountPercentage
    tsuContents = CRSDiscountPercentage
    glBuilding = CRSDiscountPercentage
    glContents = CRSDiscountPercentage
    ceBuilding = CRSDiscountPercentage
    ceContents = CRSDiscountPercentage
    allPerils = CRSDiscountPercentage

    CRSDiscountPercResults_dict = {"items": item21,
                                   "ifBuilding": ifBuilding, "ifContents": ifContents,
                                   "ssBuilding": ssBuilding, "ssContents": ssContents,
                                   "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                   "glBuilding": glBuilding, "glContents": glContents,
                                   "ceBuilding": ceBuilding, "ceContents": ceContents,
                                   "allPerils": allPerils}

    # print("CRSDiscountPercResults_dict  : ", CRSDiscountPercResults_dict)
    CRSDiscountPercResults = riskrating2results(items=item21,
                                                inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                allPerilsAllCoverage=allPerils)
    CRSDiscountPercResults.save()

    # CRS Discount Factor
    CRSDiscountFactor = 1-float(inputs['CRS discount']/100)
    item22 = "CRS Discount Factor"
    ifBuilding = CRSDiscountFactor
    ifContents = CRSDiscountFactor
    ssBuilding = CRSDiscountFactor
    ssContents = CRSDiscountFactor
    tsuBuilding = CRSDiscountFactor
    tsuContents = CRSDiscountFactor
    glBuilding = CRSDiscountFactor
    glContents = CRSDiscountFactor
    ceBuilding = CRSDiscountFactor
    ceContents = CRSDiscountFactor
    allPerils = CRSDiscountFactor

    CRSDiscountFactorResults_dict = {"items": item22,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("CRSDiscountFactorResults_dict  : ", CRSDiscountFactorResults_dict)
    CRSDiscountFactorResults = riskrating2results(items=item22,
                                                  inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                  stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                  tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                  greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                  coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                  allPerilsAllCoverage=allPerils)
    CRSDiscountFactorResults.save()

    # Geographic Rate by Peril & Coverage
    componentList = ['ifBuilding', 'ifContents', 'ssBuilding', 'ssContents', 'tsuBuilding',
                     'tsuContents', 'glBuilding', 'glContents', 'ceBuilding', 'ceContents', 'allPerils']

    geographicRatebyPerilCoverage = []
    for x in componentList:
        geoRatingFuncList = [baserateResults_dict[x], distToRiverResults_dict[x], elevRelToRiverResults_dict[x], drainageAreaResults_dict[x], strucRelElvResults_dict[x],
                             distToCoastResults_dict[x], distToOceanResults_dict[x], elevationResults_dict[x], disttolakeResults_dict[x], elevationRelToLakeResults_dict[x], territoryResults_dict[x]]
        y = 1
        for i in range(len(geoRatingFuncList)):
            if geoRatingFuncList[i] not in ['', -9999.0]:
                y *= geoRatingFuncList[i]
        geographicRatebyPerilCoverage.append(round(y, 4))

    item23 = "Geographic Rate by Peril & Coverage"
    segment = ''

    ifBuilding = geographicRatebyPerilCoverage[0]
    ifContents = geographicRatebyPerilCoverage[1]
    ssBuilding = geographicRatebyPerilCoverage[2]
    ssContents = geographicRatebyPerilCoverage[3]
    tsuBuilding = geographicRatebyPerilCoverage[4]
    tsuContents = geographicRatebyPerilCoverage[5]
    glBuilding = geographicRatebyPerilCoverage[6]
    glContents = geographicRatebyPerilCoverage[7]
    ceBuilding = geographicRatebyPerilCoverage[8]
    ceContents = geographicRatebyPerilCoverage[9]
    allPerils = ''

    geographicRateResults_dict = {"items": item23,
                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                  "glBuilding": glBuilding, "glContents": glContents,
                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                  "allPerils": allPerils}

    # print("geographicRateResults_dict  : ", geographicRateResults_dict)
    geographicRateResults = riskrating2results(items=item23,
                                               inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                               coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                               )
    geographicRateResults.save()

    # Rate by Peril & Coverage
    ratebyPerilCoverage = []
    for x in componentList:
        # print(x)
        RatingFuncList = [geographicRateResults_dict[x], typeOfUseResults_dict[x], floorsOfIntResults_dict[x], foundationResults_dict[x], firstFloorHeightResults_dict[x],
                          meAbovefirstFloorResults_dict[x], coverageValueFactorResults_dict[x],  deductibleLimittoCoverageValueResults_dict[x]]
        print("RatingFuncList = ", RatingFuncList)
        y = 1
        for i in range(len(RatingFuncList)):
            if RatingFuncList[i] not in ['', -9999.0]:
                y *= RatingFuncList[i]
        ratebyPerilCoverage.append(round(y, 4))
    print("RatebyPerilCoverage = ", ratebyPerilCoverage)

    print("firstFloorHeightResults_dict = ",
          firstFloorHeightResults_dict.values())
    print("coverageValueFactorResults_dict = ",
          coverageValueFactorResults_dict.values())
    print("ratebyPerilCoverage = ", ratebyPerilCoverage)

    ratebyPerilCoverage1 = []
    for i, x in enumerate(componentList):
        if not (x == 'allPerils'):
            a = float(finalDeductibleITVResults_dict[x])
            b = float(CRSDiscountFactorResults_dict[x])
            c = float(ratebyPerilCoverage[i])

            y = a * b * c
            ratebyPerilCoverage1.append(round(y, 4))
    print("RatebyPerilCoverage1 = ", ratebyPerilCoverage1)

    ratebyPerilCoverage1[0] = float(
        ratebyPerilCoverage1[0])*float(concRiskResults_dict['ifBuilding'])
    ratebyPerilCoverage1[1] = float(
        ratebyPerilCoverage1[1])*float(concRiskResults_dict['ifContents'])
    ratebyPerilCoverage1[2] = float(
        ratebyPerilCoverage1[2])*float(concRiskResults_dict['ssBuilding'])
    ratebyPerilCoverage1[3] = float(
        ratebyPerilCoverage1[3])*float(concRiskResults_dict['ssContents'])
    print("RatebyPerilCoverage1 = ", ratebyPerilCoverage1)

    item24 = "Rate by Peril & Coverage"
    segment = ''

    ifBuilding = ratebyPerilCoverage1[0]
    ifContents = ratebyPerilCoverage1[1]
    ssBuilding = ratebyPerilCoverage1[2]
    ssContents = ratebyPerilCoverage1[3]
    tsuBuilding = ratebyPerilCoverage1[4]
    tsuContents = ratebyPerilCoverage1[5]
    glBuilding = ratebyPerilCoverage1[6]
    glContents = ratebyPerilCoverage1[7]
    ceBuilding = ratebyPerilCoverage1[8]
    ceContents = ratebyPerilCoverage1[9]
    allPerils = ''

    ratebyPerilCoverageResults_dict = {"items": item24, "Segment": segment,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("ratebyPerilCoverageResults_dict  : ", ratebyPerilCoverageResults_dict)
    ratebyPerilCoverageResults = riskrating2results(items=item24,
                                                    inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                    stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                    tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                    greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                    coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                    )
    ratebyPerilCoverageResults.save()

    Rate_of_building = round((ratebyPerilCoverage1[0] +
                              ratebyPerilCoverage1[2] +
                              ratebyPerilCoverage1[4] +
                              ratebyPerilCoverage1[6] +
                              ratebyPerilCoverage1[8]), 4)

    item25 = "Rate (per $1000 of Building Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = Rate_of_building

    rateBuildingValueResults_dict = {"items": item25,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("rateBuildingValueResults_dict  : ", rateBuildingValueResults_dict)
    rateBuildingValueResults = riskrating2results(items=item25,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    rateBuildingValueResults.save()

    Rate_of_contents = round((ratebyPerilCoverage1[1] +
                              ratebyPerilCoverage1[3] +
                              ratebyPerilCoverage1[5] +
                              ratebyPerilCoverage1[7] +
                              ratebyPerilCoverage1[9]), 4)

    item26 = "Rate (per $1000 of Contents Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = Rate_of_contents

    rateContentsValueResults_dict = {"items": item26,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("rateContentsValueResults_dict  : ", rateContentsValueResults_dict)
    rateContentsValueResults = riskrating2results(items=item26,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    rateContentsValueResults.save()

    ifBuilding_WbyC = round(
        (ratebyPerilCoverage1[0] / Rate_of_building)*100, 4)
    ifContents_WbyC = round(
        (ratebyPerilCoverage1[1] / Rate_of_contents)*100, 4)
    ssBuilding_WbyC = round(
        (ratebyPerilCoverage1[2] / Rate_of_building)*100, 4)
    ssContents_WbyC = round(
        (ratebyPerilCoverage1[3] / Rate_of_contents)*100, 4)
    tsuBuilding_WbyC = round(
        (ratebyPerilCoverage1[4] / Rate_of_building)*100, 4)
    tsuContents_WbyC = round(
        (ratebyPerilCoverage1[5] / Rate_of_contents)*100, 4)
    glBuilding_WbyC = round(
        (ratebyPerilCoverage1[6] / Rate_of_building)*100, 4)
    glContents_WbyC = round(
        (ratebyPerilCoverage1[7] / Rate_of_contents)*100, 4)
    ceBuilding_WbyC = round(
        (ratebyPerilCoverage1[8] / Rate_of_building)*100, 4)
    ceContents_WbyC = round(
        (ratebyPerilCoverage1[9] / Rate_of_contents)*100, 4)

    item27 = "Rate Weights by Coverage"
    ifBuilding = ifBuilding_WbyC
    ifContents = ifContents_WbyC
    ssBuilding = ssBuilding_WbyC
    ssContents = ssContents_WbyC
    tsuBuilding = tsuBuilding_WbyC
    tsuContents = tsuContents_WbyC
    glBuilding = glBuilding_WbyC
    glContents = glContents_WbyC
    ceBuilding = ceBuilding_WbyC
    ceContents = ceContents_WbyC
    allPerils = ''

    rateWeightsbyCoverageResults_dict = {"items": item27,
                                         "ifBuilding": ifBuilding, "ifContents": ifContents,
                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                         "glBuilding": glBuilding, "glContents": glContents,
                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                         "allPerils": allPerils}

    # print("rateWeightsbyCoverageResults_dict  : ", rateWeightsbyCoverageResults_dict)
    rateWeightsbyCoverageResults = riskrating2results(items=item27,
                                                      inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                      stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                      tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                      greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                      coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                      )
    rateWeightsbyCoverageResults.save()

    weighted_deductible_building = round((float(finalDeductibleITVResults_dict['ifBuilding']) * ifBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['ssBuilding']) * ssBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['tsuBuilding']) * tsuBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['glBuilding']) * glBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['ceBuilding']) * ceBuilding_WbyC)/100, 4)

    item28 = "Weighted Deductible & ITV Factor (Building)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = weighted_deductible_building

    weightedDeductibleITVBuildingResults_dict = {"items": item28,
                                                 "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                 "glBuilding": glBuilding, "glContents": glContents,
                                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                 "allPerils": allPerils}

    # print("weightedDeductibleITVBuildingResults_dict  : ", weightedDeductibleITVBuildingResults_dict)
    weightedDeductibleITVBuildingResults = riskrating2results(items=item28,
                                                              allPerilsAllCoverage=allPerils
                                                              )
    weightedDeductibleITVBuildingResults.save()

    weighted_deductible_contents = round((float(finalDeductibleITVResults_dict['ifContents']) * ifContents_WbyC +
                                          float(finalDeductibleITVResults_dict['ssContents']) * ssContents_WbyC +
                                          float(finalDeductibleITVResults_dict['tsuContents']) * tsuContents_WbyC +
                                          float(finalDeductibleITVResults_dict['glContents']) * glContents_WbyC +
                                          float(finalDeductibleITVResults_dict['ceContents']) * ceContents_WbyC)/100, 4)

    item29 = "Weighted Deductible & ITV Factor (Contents)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = weighted_deductible_contents

    weightedDeductibleITVContentsResults_dict = {"items": item29,
                                                 "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                 "glBuilding": glBuilding, "glContents": glContents,
                                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                 "allPerils": allPerils}

    # print("weightedDeductibleITVContentsResults_dict  : ", weightedDeductibleITVContentsResults_dict)
    weightedDeductibleITVContentsResults = riskrating2results(items=item29,
                                                              allPerilsAllCoverage=allPerils
                                                              )
    weightedDeductibleITVContentsResults.save()

    min_rate_building = round(0 * weighted_deductible_building, 4)
    max_rate_building = round(15 * weighted_deductible_building, 4)

    item30 = "Minimum Rate (per $1000 of Building Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = min_rate_building

    min_rate_buildingResults_dict = {"items": item30,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("min_rate_buildingResults_dict  : ", min_rate_buildingResults_dict)
    min_rate_buildingResults = riskrating2results(items=item30,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    min_rate_buildingResults.save()

    item31 = "Maximum Rate (per $1000 of Building Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = max_rate_building

    max_rate_buildingResults_dict = {"items": item31,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("max_rate_buildingResults_dict  : ", max_rate_buildingResults_dict)
    max_rate_buildingResults = riskrating2results(items=item31,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    max_rate_buildingResults.save()

    min_rate_contents = round(0 * weighted_deductible_contents, 4)
    max_rate_contents = round(15 * weighted_deductible_contents, 4)

    item32 = "Minimum Rate (per $1000 of Contents Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = min_rate_contents

    min_rate_contentsResults_dict = {"items": item32,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("min_rate_contentsResults_dict  : ", min_rate_contentsResults_dict)
    min_rate_contentsResults = riskrating2results(items=item32,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    min_rate_contentsResults.save()

    item33 = "Maximum Rate (per $1000 of Contents Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = max_rate_contents

    max_rate_contentsResults_dict = {"items": item33,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("max_rate_contentsResults_dict  : ", max_rate_contentsResults_dict)
    max_rate_contentsResults = riskrating2results(items=item33,
                                                  allPerilsAllCoverage=allPerils
                                                  )
    max_rate_contentsResults.save()

    ############
    item34 = "Minimum Rate by Peril & Coverage (per $1000 of Coverage Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    min_rate_PerilCoverageResults_dict = {"items": item34,
                                          "ifBuilding": ifBuilding, "ifContents": ifContents,
                                          "ssBuilding": ssBuilding, "ssContents": ssContents,
                                          "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                          "glBuilding": glBuilding, "glContents": glContents,
                                          "ceBuilding": ceBuilding, "ceContents": ceContents,
                                          "allPerils": allPerils}

    # print("min_rate_PerilCoverageResults_dict  : ", min_rate_PerilCoverageResults_dict)
    min_rate_PerilCoverageResults = riskrating2results(items=item34,
                                                       )
    min_rate_PerilCoverageResults.save()

    item35 = "Maximum Rate by Peril & Coverage (per $1000 of Coverage Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    max_rate_PerilCoverageResults_dict = {"items": item35,
                                          "ifBuilding": ifBuilding, "ifContents": ifContents,
                                          "ssBuilding": ssBuilding, "ssContents": ssContents,
                                          "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                          "glBuilding": glBuilding, "glContents": glContents,
                                          "ceBuilding": ceBuilding, "ceContents": ceContents,
                                          "allPerils": allPerils}

    # print("max_rate_PerilCoverageResults_dict  : ", max_rate_PerilCoverageResults_dict)
    max_rate_PerilCoverageResults = riskrating2results(items=item35
                                                       )
    max_rate_PerilCoverageResults.save()

    ############

    final_rate_building = min(
        max(Rate_of_building, min_rate_building), max_rate_building)
    final_rate_contents = min(
        max(Rate_of_contents, min_rate_contents), max_rate_contents)

    item36 = "Final Rate (per $1000 of Building Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = final_rate_building

    final_rate_buildingResults_dict = {"items": item36,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("final_rate_buildingResults_dict  : ", final_rate_buildingResults_dict)
    final_rate_buildingResults = riskrating2results(items=item36,
                                                    allPerilsAllCoverage=allPerils
                                                    )
    final_rate_buildingResults.save()

    item37 = "Final Rate (per $1000 of Contents Value)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = final_rate_contents

    final_rate_contentsResults_dict = {"items": item37,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("final_rate_contentsResults_dict  : ", final_rate_contentsResults_dict)
    final_rate_contentsResults = riskrating2results(items=item37,
                                                    allPerilsAllCoverage=allPerils
                                                    )
    final_rate_contentsResults.save()

    coverage_building_thousands = inputs['Coverage A value']/1000
    coverage_contents_thousands = inputs['Coverage C value']/1000
    initial_premium_without_fees_building = final_rate_building * \
        coverage_building_thousands
    initial_premium_without_fees_contents = final_rate_contents * \
        coverage_contents_thousands
    initial_premium_without_fees = initial_premium_without_fees_building + \
        initial_premium_without_fees_contents
    prior_claim_premium = (inputs['Prior Claim Rate'] * coverage_building_thousands *
                           weighted_deductible_building * max(0, inputs['Prior claims']-1))
    premium_exc_fees_expense = initial_premium_without_fees + prior_claim_premium
    premium_without_fees = premium_exc_fees_expense + \
        inputs['Loss Constant'] + inputs['Expense Constant']
    icc_crs = inputs['ICC premium'] * (100-inputs['CRS discount'])/100
    subtotal = (premium_without_fees + icc_crs)

#     risk_rating_2.iloc[39,11] = coverage_building_thousands

    item38 = "Coverage Value in Thousands (Buildings)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = coverage_building_thousands

    coverage_building_thousandsfinal_rate_contentsResults_dict = {"items": item37,
                                                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                                  "glBuilding": glBuilding, "glContents": glContents,
                                                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                                  "allPerils": allPerils}

    # print("coverage_building_thousandsResults_dict  : ", coverage_building_thousandsResults_dict)
    coverage_building_thousandsResults = riskrating2results(items=item37,
                                                            allPerilsAllCoverage=allPerils
                                                            )
    coverage_building_thousandsResults.save()

#     risk_rating_2.iloc[40,11] = coverage_contents_thousands
    item39 = "Coverage Value in Thousands (Contents)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = coverage_contents_thousands

    coverage_contents_thousandsResults_dict = {"items": item39,
                                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                               "glBuilding": glBuilding, "glContents": glContents,
                                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                                               "allPerils": allPerils}

    # print("coverage_contents_thousandsResults_dict  : ", coverage_contents_thousandsResults_dict)
    coverage_contents_thousandsResults = riskrating2results(items=item39,
                                                            allPerilsAllCoverage=allPerils
                                                            )
    coverage_contents_thousandsResults.save()


#     risk_rating_2.iloc[41,11] = initial_premium_without_fees_building
    item40 = "Initial Premium without Fees (Buildings)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees_building
    initial_premium_without_fees_buildingResults_dict = {"items": item40,
                                                         "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                         "glBuilding": glBuilding, "glContents": glContents,
                                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                         "allPerils": allPerils}

    # print("initial_premium_without_fees_buildingResults_dict  : ", initial_premium_without_fees_buildingResults_dict)
    initial_premium_without_fees_buildingResults = riskrating2results(items=item40,
                                                                      allPerilsAllCoverage=allPerils
                                                                      )
    initial_premium_without_fees_buildingResults.save()

#     risk_rating_2.iloc[42,11] = initial_premium_without_fees_contents
    item41 = "Initial Premium without Fees (Contents)"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees_contents

    initial_premium_without_fees_contentsResults_dict = {"items": item41,
                                                         "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                         "glBuilding": glBuilding, "glContents": glContents,
                                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                         "allPerils": allPerils}

    # print("initial_premium_without_fees_contentsResults_dict  : ", initial_premium_without_fees_contentsResults_dict)
    initial_premium_without_fees_contentsResults = riskrating2results(items=item41,
                                                                      allPerilsAllCoverage=allPerils
                                                                      )
    initial_premium_without_fees_contentsResults.save()


#     risk_rating_2.iloc[43,11] = initial_premium_without_fees
    item42 = "Initial Premium without Fees"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees

    initial_premium_without_feesResults_dict = {"items": item42,
                                                "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                "glBuilding": glBuilding, "glContents": glContents,
                                                "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                "allPerils": allPerils}

    # print("initial_premium_without_feesResults_dict  : ", initial_premium_without_feesResults_dict)
    initial_premium_without_feesResults = riskrating2results(items=item42,
                                                             allPerilsAllCoverage=allPerils
                                                             )
    initial_premium_without_feesResults.save()


#     risk_rating_2.iloc[44,11] = prior_claim_premium
    item43 = "Prior Claims Premium"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = prior_claim_premium

    prior_claim_premiumResults_dict = {"items": item43,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("prior_claim_premiumResults_dict  : ", prior_claim_premiumResults_dict)
    prior_claim_premiumResults = riskrating2results(items=item43,
                                                    allPerilsAllCoverage=allPerils
                                                    )
    prior_claim_premiumResults.save()


#     risk_rating_2.iloc[45,11] = premium_exc_fees_expense
    item44 = "Premium excluding Fees & Expense Constant"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium_exc_fees_expense

    premium_exc_fees_expenseResults_dict = {"items": item44,
                                            "ifBuilding": ifBuilding, "ifContents": ifContents,
                                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                            "glBuilding": glBuilding, "glContents": glContents,
                                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                                            "allPerils": allPerils}

    # print("premium_exc_fees_expenseResults_dict  : ", premium_exc_fees_expenseResults_dict)
    premium_exc_fees_expenseResults = riskrating2results(items=item44,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    premium_exc_fees_expenseResults.save()

#     risk_rating_2.iloc[46,11] = inputs['Expense Constant']
    item45 = "Expense Constant"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Expense Constant']

    expense_ConstantResults_dict = {"items": item45,
                                    "ifBuilding": ifBuilding, "ifContents": ifContents,
                                    "ssBuilding": ssBuilding, "ssContents": ssContents,
                                    "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                    "glBuilding": glBuilding, "glContents": glContents,
                                    "ceBuilding": ceBuilding, "ceContents": ceContents,
                                    "allPerils": allPerils}

    # print("expense_ConstantResults_dict  : ", expense_ConstantResults_dict)
    expense_ConstantResults = riskrating2results(items=item45,
                                                 allPerilsAllCoverage=allPerils
                                                 )
    expense_ConstantResults.save()

#     risk_rating_2.iloc[47,11] = inputs['Loss Constant']
    item46 = "Loss Constant"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Loss Constant']

    loss_ConstantResults_dict = {"items": item46,
                                 "ifBuilding": ifBuilding, "ifContents": ifContents,
                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                 "glBuilding": glBuilding, "glContents": glContents,
                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                 "allPerils": allPerils}

    # print("loss_ConstantResults_dict  : ", loss_ConstantResults_dict)
    loss_ConstantResults = riskrating2results(items=item46,
                                              allPerilsAllCoverage=allPerils
                                              )
    loss_ConstantResults.save()

#     risk_rating_2.iloc[48,11] = premium_without_fees
    item47 = "Premium without Fees"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium_without_fees

    premium_without_feesResults_dict = {"items": item47,
                                        "ifBuilding": ifBuilding, "ifContents": ifContents,
                                        "ssBuilding": ssBuilding, "ssContents": ssContents,
                                        "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                        "glBuilding": glBuilding, "glContents": glContents,
                                        "ceBuilding": ceBuilding, "ceContents": ceContents,
                                        "allPerils": allPerils}

    # print("premium_without_feesResults_dict  : ", premium_without_feesResults_dict)
    premium_without_feesResults = riskrating2results(items=item47,
                                                     allPerilsAllCoverage=allPerils
                                                     )
    premium_without_feesResults.save()


#     risk_rating_2.iloc[49,11] = inputs['ICC premium']
    item48 = "ICC Premium"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['ICC premium']

    icc_premiumResults_dict = {"items": item48,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("icc_premiumResults_dict  : ", icc_premiumResults_dict)
    icc_premiumResults = riskrating2results(items=item48,
                                            allPerilsAllCoverage=allPerils
                                            )
    icc_premiumResults.save()

#     risk_rating_2.iloc[50,11] = icc_crs
    item49 = "ICC Premium with CRS Discount"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = icc_crs

    icc_crsResults_dict = {"items": item49,
                           "ifBuilding": ifBuilding, "ifContents": ifContents,
                           "ssBuilding": ssBuilding, "ssContents": ssContents,
                           "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                           "glBuilding": glBuilding, "glContents": glContents,
                           "ceBuilding": ceBuilding, "ceContents": ceContents,
                           "allPerils": allPerils}

    # print("icc_crsResults_dict  : ", icc_crsResults_dict)
    icc_crsResults = riskrating2results(items=item49,
                                        allPerilsAllCoverage=allPerils
                                        )
    icc_crsResults.save()

#     risk_rating_2.iloc[51,11] = subtotal
    item50 = "Subtotal"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = subtotal

    subtotalResults_dict = {"items": item50,
                            "ifBuilding": ifBuilding, "ifContents": ifContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}

    # print("subtotalResults_dict  : ", subtotalResults_dict)
    subtotalResults = riskrating2results(items=item50,
                                         allPerilsAllCoverage=allPerils
                                         )
    subtotalResults.save()

#     risk_rating_2.iloc[52,11] = inputs['Reserve fund']
    item51 = "Reserve Fund Factor"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Reserve fund']

    reserve_fund_factorResults_dict = {"items": item51,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("reserve_fund_factorResults_dict  : ", reserve_fund_factorResults_dict)
    reserve_fund_factorResults = riskrating2results(items=item51,
                                                    allPerilsAllCoverage=allPerils
                                                    )
    reserve_fund_factorResults.save()

    # subtotal = subtotal * inputs['Reserve fund']
    # risk_rating_2.iloc[53,11] = subtotal
    subtotal_with_reservefund = subtotal * inputs['Reserve fund']

    item52 = "Subtotal with Reserve Fund"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = subtotal_with_reservefund

    subtotal_with_reservefundResults_dict = {"items": item52,
                                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                             "glBuilding": glBuilding, "glContents": glContents,
                                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                                             "allPerils": allPerils}

    # print("subtotal_with_reservefundResults_dict  : ", subtotal_with_reservefundResults_dict)
    subtotal_with_reservefundResults = riskrating2results(items=item52,
                                                          allPerilsAllCoverage=allPerils
                                                          )
    subtotal_with_reservefundResults.save()

#     risk_rating_2.iloc[54,11] = inputs['Probation surcharge']
    item53 = "Probation Surcharge"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Probation surcharge']

    probation_surchargeResults_dict = {"items": item53,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("probation_surchargeResults_dict  : ", probation_surchargeResults_dict)
    probation_surchargeResults = riskrating2results(items=item53,
                                                    allPerilsAllCoverage=allPerils
                                                    )
    probation_surchargeResults.save()

    if inputs['Primary residence indicator'] == 'Yes':
        HFIAA_surcharge = 50
    else:
        HFIAA_surcharge = 250
#     risk_rating_2.iloc[55,11] = HFIAA_surcharge
    item54 = "HFIAA Surcharge by Primary Residence Indicator"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = HFIAA_surcharge

    hfiaa_surchargeResults_dict = {"items": item54,
                                   "ifBuilding": ifBuilding, "ifContents": ifContents,
                                   "ssBuilding": ssBuilding, "ssContents": ssContents,
                                   "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                   "glBuilding": glBuilding, "glContents": glContents,
                                   "ceBuilding": ceBuilding, "ceContents": ceContents,
                                   "allPerils": allPerils}

    # print("hfiaa_surchargeResults_dict  : ", hfiaa_surchargeResults_dict)
    hfiaa_surchargeResults = riskrating2results(items=item54,
                                                allPerilsAllCoverage=allPerils
                                                )
    hfiaa_surchargeResults.save()

#     risk_rating_2.iloc[56,11] = inputs['Federal policy fee']
    item55 = "Federal Policy Fee"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Federal policy fee']

    federal_policy_feeResults_dict = {"items": item55,
                                      "ifBuilding": ifBuilding, "ifContents": ifContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}

    # print("federal_policy_feeResults_dict  : ", federal_policy_feeResults_dict)
    federal_policy_feeResults = riskrating2results(items=item55,
                                                   allPerilsAllCoverage=allPerils
                                                   )
    federal_policy_feeResults.save()

    premium = round(subtotal_with_reservefund + inputs['Probation surcharge'] +
                    HFIAA_surcharge + inputs['Federal policy fee'], 2)
#     risk_rating_2.iloc[57,11] = premium
    item56 = "Premium with Fees"
    ifBuilding = ''
    ifContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium

    premiumResults_dict = {"items": item56,
                           "ifBuilding": ifBuilding, "ifContents": ifContents,
                           "ssBuilding": ssBuilding, "ssContents": ssContents,
                           "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                           "glBuilding": glBuilding, "glContents": glContents,
                           "ceBuilding": ceBuilding, "ceContents": ceContents,
                           "allPerils": allPerils}

    # print("premiumResults_dict  : ", premiumResults_dict)
    premiumResults = riskrating2results(items=item56,
                                        allPerilsAllCoverage=allPerils
                                        )
    premiumResults.save()

#     return risk_rating_2

    return [{"baserate results": baserateResults_dict}, {"distToRiver results": distToRiverResults_dict},
            {"elevRelToRiver results": elevRelToRiverResults_dict}, {
                "drainageArea results": drainageAreaResults_dict},
            {"strucRelElv results": strucRelElvResults_dict}, {
                "distToCoast results": distToCoastResults_dict},
            {"distToOcean results": distToOceanResults_dict}, {
                "elevation results": elevationResults_dict}, {"disttolake results": disttolakeResults_dict},
            {"elevationRelToLake results": elevationRelToLakeResults_dict},
            {"territory results": territoryResults_dict}, {
                "typeOfUse results": typeOfUseResults_dict},
            {"floorsOfInt results": floorsOfIntResults_dict}, {
                "foundation results": foundationResults_dict},
            {"firstFloorHeight results": firstFloorHeightResults_dict}, {
                "meAbovefirstFloor results": meAbovefirstFloorResults_dict},
            {"coverageValueFactor results": coverageValueFactorResults_dict},
            {"deductibleLimittoCoverage results": deductibleLimittoCoverageValueResults_dict}, {
                "deductibletoCoverage results": deductibletoCoverageValueResults_dict},
            {"initialDeductibleITV results": initialDeductibleITVResults_dict}, {
                "finalDeductibleITV results": finalDeductibleITVResults_dict},
            {"Concentration Risk Results": concRiskResults_dict}, {"CRS Discount Percentage Results":
                                                                   CRSDiscountPercResults_dict}, {"CRS Discount Factor Results": CRSDiscountFactorResults_dict},
            {"Geographic Rate Results": geographicRateResults_dict},
            {"rate by Peril Coverage Results": ratebyPerilCoverageResults_dict},
            {"Rate Building Value Results Dict": rateBuildingValueResults_dict},
            {"Rate Contents Value Results Dict": rateContentsValueResults_dict},
            {"Rate Weights by Coverage Results Dict": rateWeightsbyCoverageResults_dict},
            {"weighted Deductible ITV Building Results Dict": weightedDeductibleITVBuildingResults_dict},
            {"weighted Deductible ITV Contents Results Dict": weightedDeductibleITVContentsResults_dict},
            {"min_rate_building Results Dict": min_rate_buildingResults_dict},
            {"max_rate_building Results Dict": max_rate_buildingResults_dict},
            {"min_rate_contents Results Dict": min_rate_contentsResults_dict},
            {"max_rate_contents Results Dict": max_rate_contentsResults_dict},
            {"min_rate_PerilCoverage Results Dict": min_rate_PerilCoverageResults_dict},
            {"max_rate_PerilCoverage Results Dict": max_rate_PerilCoverageResults_dict},
            {"final_rate_building Results Dict": final_rate_buildingResults_dict},
            {"final_rate_contents Results Dict": final_rate_contentsResults_dict},
            {"coverage_building_thousandsfinal_rate_contentsResults_dict":
                coverage_building_thousandsfinal_rate_contentsResults_dict},
            {"coverage_contents_thousandsResults_dict": coverage_contents_thousandsResults_dict},
            {"initial_premium_without_fees_buildingResults_dict":
                initial_premium_without_fees_buildingResults_dict},
            {"initial_premium_without_fees_contentsResults_dict":
                initial_premium_without_fees_contentsResults_dict},
            {"initial_premium_without_feesResults_dict": initial_premium_without_feesResults_dict},
            {"prior_claim_premiumResults_dict": prior_claim_premiumResults_dict},
            {"premium_exc_fees_expenseResults_dict": premium_exc_fees_expenseResults_dict},
            {"expense_ConstantResults_dict": expense_ConstantResults_dict},
            {"loss_ConstantResults_dict": loss_ConstantResults_dict},
            {"premium_without_feesResults_dict": premium_without_feesResults_dict},
            {"icc_premiumResults_dict": icc_premiumResults_dict},
            {"icc_crsResults_dict": icc_crsResults_dict},
            {"subtotalResults_dict": subtotalResults_dict},
            {"reserve_fund_factorResults_dict": reserve_fund_factorResults_dict},
            {"subtotal_with_reservefundResults_dict": subtotal_with_reservefundResults_dict},
            {"probation_surchargeResults_dict": probation_surchargeResults_dict},
            {"hfiaa_surchargeResults_dict": hfiaa_surchargeResults_dict},
            {"federal_policy_feeResults_dict": federal_policy_feeResults_dict},
            {"premiumResults_dict": premiumResults_dict}]
