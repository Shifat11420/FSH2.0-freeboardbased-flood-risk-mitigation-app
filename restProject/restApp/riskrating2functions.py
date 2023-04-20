from .models import *
from rest_framework.response import Response
import pandas as pd
import numpy as np
from django.db.models import Q


def baserate(inputs):
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

    baserateResults_dict = {"items": item1, "Segment": segment,
                            "ifBuilding": ifBuilding, "ifContents": ifContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents}
    # print("baserate Results  : ", baserateResults_dict)

    baseRateResult = riskrating2results(items=item1,
                                        inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                        stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                        tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                        greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                        coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                        )
    baseRateResult.save()
    return [{"results": baserateResults_dict}]


def distToRiver(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

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
    print("B = ", B)

    item2 = "Distance to River"
    segment = ''
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

    distToRiverResults_dict = {"items": item2, "Segment": segment,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("distToRiver Results  : ", distToRiverResults_dict)
    distToRiverResult = riskrating2results(items=item2,
                                           inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    distToRiverResult.save()
    return [{"results": distToRiverResults_dict}]


def elevRelToRiverfunc(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

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
    print("C = ", C)

    item3 = "Elevation Relative to River by River Class"
    segment = ''
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

    elevRelToRiverResults_dict = {"items": item3, "Segment": segment,
                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                  "glBuilding": glBuilding, "glContents": glContents,
                                  "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("elevRelToRiverResults_dict  : ", elevRelToRiverResults_dict)
    elevRelToRiverResults = riskrating2results(items=item3,
                                               inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    elevRelToRiverResults.save()
    return [{"results": elevRelToRiverResults_dict}]


def drainageAreafunc(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

    drainArea = drainageAreaMultipliers.objects.filter(
        levee=inputs['Levee'], segment=segmentfromBaserate).all()

    da_km2 = drainArea.values_list("da_km2", flat=True)
    da_km2 = list(da_km2)
    ifvalue = drainArea.values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    D = np.interp([inputs['DA']], da_km2, ifvalue)
    print("D = ", D)

    item4 = "Drainage Area"
    segment = ''
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

    drainageAreaResults_dict = {"items": item4, "Segment": segment,
                                "ifBuilding": ifBuilding, "ifContents": ifContents,
                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                "glBuilding": glBuilding, "glContents": glContents,
                                "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("drainageAreaResults_dict  : ", drainageAreaResults_dict)
    drainageAreaResults = riskrating2results(items=item4,
                                             inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    drainageAreaResults.save()
    return [{"results": drainageAreaResults_dict}]


def strucRelElevfunc(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

    strucRelElv = structuralRelElevation.objects.filter(
        levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate)).all()

    sre_feet = strucRelElv .values_list("sre_feet", flat=True)
    sre_feet = list(sre_feet)
    ifvalue = strucRelElv .values_list("ifvalue", flat=True)
    ifvalue = list(ifvalue)

    E = np.interp([inputs['SRE']], sre_feet, ifvalue)
    print("E = ", round(float(E), 4))

    item5 = "Structural Relative Elevation"
    segment = ''
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

    strucRelElvResults_dict = {"items": item5, "Segment": segment,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("strucRelElvResults_dict  : ", strucRelElvResults_dict)
    strucRelElvResults = riskrating2results(items=item5,
                                            inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents)
    strucRelElvResults.save()
    return [{"results": strucRelElvResults_dict}]


def distanceToCoast(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

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
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), BI=inputs['Barrier island indicator']).all()
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
    segment = ''
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

    distToCoastResults_dict = {"items": item6, "Segment": segment,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("distToCoastResults_dict  : ", distToCoastResults_dict)
    distToCoastResults = riskrating2results(items=item6,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                            coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents)
    distToCoastResults.save()
    return [{"results": distToCoastResults_dict}]


def distanceToOcean(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

    if segmentfromBaserate != 3 and segmentfromBaserate != 4 and inputs['DTO'] != 'N/A':
        dto = distToOceanMultipliers.objects.filter(
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), BI=inputs['Barrier island indicator']).all()
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
    segment = ''
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

    distToOceanResults_dict = {"items": item7, "Segment": segment,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("distToOceanResults_dict  : ", distToOceanResults_dict)
    distToOceanResults = riskrating2results(items=item7,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents
                                            )
    distToOceanResults.save()
    return [{"results": distToOceanResults_dict}]


def elevationfunc(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']

    if segmentfromBaserate != 3 and segmentfromBaserate != 4:
        elev = elevation.objects.filter(
            levee=inputs['Levee'], region='Segment '+str(segmentfromBaserate), BI=inputs['Barrier island indicator']).all()
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
    segment = ''
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

    elevationResults_dict = {"items": item8, "Segment": segment,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("elevationResults_dict  : ", elevationResults_dict)
    elevationResults = riskrating2results(items=item8,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents
                                          )
    elevationResults.save()
    return [{"results": elevationResults_dict}]


def distanceToLake(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']
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
    segment = ''
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

    disttolakeResults_dict = {"items": item9, "Segment": segment,
                              "ifBuilding": ifBuilding, "ifContents": ifContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("disttolakeResults_dict  : ", disttolakeResults_dict)
    disttolakeResults = riskrating2results(items=item9,
                                           greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                           )
    disttolakeResults.save()
    return [{"results": disttolakeResults_dict}]


def elevationRelToLake(inputs):
    segmentfromBaserate = baserate(inputs)[0]['results']['Segment']
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
    segment = ''
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

    elevationRelToLakeResults_dict = {"items": item10, "Segment": segment,
                                      "ifBuilding": ifBuilding, "ifContents": ifContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("elevationRelToLakeResults_dict  : ", elevationRelToLakeResults_dict)
    elevationRelToLakeResults = riskrating2results(items=item10,
                                                   greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                   )
    elevationRelToLakeResults.save()
    return [{"results": elevationRelToLakeResults_dict}]


def territoryfunc(inputs):
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
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), peril='IF').all()

    territory_if = territory_huc12_if.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_if = list(territory_if)
    ifBldg = round(territory_if[0], 4)
    ifCont = round(territory_if[0], 4)

    # SS
    territory_huc12_ss = territory.objects.filter(
        levee=inputs['Levee'], huc12=int(inputs['HUC12']), peril='SS').all()

    territory_ss = territory_huc12_ss.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_ss = list(territory_ss)
    ssBldg = round(territory_ss[0], 4)
    ssCont = round(territory_ss[0], 4)

    item11 = "Territory (HUC12 & Barrier Island Indicator)"
    segment = ''
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

    territoryResults_dict = {"items": item11, "Segment": segment,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("territoryResults_dict  : ", territoryResults_dict)
    territoryResults = riskrating2results(items=item11,
                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                          )
    territoryResults.save()
    return [{"results": territoryResults_dict}]


def typeOfUsefunc(inputs):
    typeuse = typeOfUSe.objects.filter(
        typeofuse=inputs['Type of Use']).all()

    typeuse_if = typeuse.values_list('flood', flat=True)
    typeuse_if = list(typeuse_if)
    typeuse_ss = typeuse.values_list('surge', flat=True)
    typeuse_ss = list(typeuse_if)
    typeuse_tsu = typeuse.values_list('tsunami', flat=True)
    typeuse_tsu = list(typeuse_if)
    typeuse_gl = typeuse.values_list('lakes', flat=True)
    typeuse_gl = list(typeuse_if)

    item12 = "Type of Use"
    segment = ''
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

    territoryResults_dict = {"items": item12, "Segment": segment,
                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("typeOfUseResults_dict  : ", typeOfUseResults_dict)
    typeOfUseResults = riskrating2results(items=item12,
                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                          )
    typeOfUseResults.save()
    return [{"results": territoryResults_dict}]


def floorsOfInterestfunc(inputs):
    floorsOfInt = floorsOfInterest.objects.filter(
        homeIndicator=inputs['Single family home indicator'], ownerIndicator=inputs['Condo unit owner indicator'], interest=inputs['Floor of interest']).all()

    floorsOfInt_allexclCE = floorsOfInt.values_list('allExclCE', flat=True)
    floorsOfInt_allexclCE = list(floorsOfInt_allexclCE)

    item12 = "Floor of Interest"
    segment = ''
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

    floorsOfIntResults_dict = {"items": item12, "Segment": segment,
                               "ifBuilding": ifBuilding, "ifContents": ifContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("floorsOfIntResults_dict  : ", floorsOfIntResults_dict)
    floorsOfIntResults = riskrating2results(items=item12,
                                            inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                            stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                            tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                            greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                            )
    floorsOfIntResults.save()
    return [{"results": floorsOfIntResults_dict}]


def foundationtypefunc(inputs):
    foundation = foundationType.objects.filter(
        foundationtypes=inputs['Foundation type']).all()

    foundation_allexclCE = foundation.values_list('allExclCE', flat=True)
    foundation_allexclCE = list(foundation_allexclCE)

    item13 = "Foundation Type"
    segment = ''
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

    foundationResults_dict = {"items": item13, "Segment": segment,
                              "ifBuilding": ifBuilding, "ifContents": ifContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("foundationResults_dict  : ", foundationResults_dict)
    foundationResults = riskrating2results(items=item13,
                                           inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                           stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                           tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                           greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                           )
    foundationResults.save()
    return [{"results": foundationResults_dict}]


def heightDesignVent(inputs):
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
    # print("floodEventyesWFV = ", floodEventyesWFV)
    # print("floodEventnoWbyFV = ", floodEventnoWbyFV)

    if inputs['Flood vents'] == "Yes":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventyesWFV)
    elif inputs['Flood vents'] == "No":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventnoWbyFV)
    P = round(float(P), 4)
    print("P = ", round(float(P), 4))

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

    firstFloorHeightResults_dict = {"items": item14, "Segment": segment,
                                    "ifBuilding": ifBuilding, "ifContents": ifContents,
                                    "ssBuilding": ssBuilding, "ssContents": ssContents,
                                    "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                    "glBuilding": glBuilding, "glContents": glContents,
                                    "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("firstFloorHeightResults_dict  : ", firstFloorHeightResults_dict)
    firstFloorHeightResults = riskrating2results(items=item14,
                                                 inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                 stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                 tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                 greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                 )
    firstFloorHeightResults.save()
    return [{"results": firstFloorHeightResults_dict}]


def MEAboveFirstFloorfunc(inputs):
    me = MEAboveFirstFloor.objects.filter(
        machineryEquipmentAboveFirstFloor=inputs['M&E']).all()

    meCE = float(me.values()[0]['coastalErosion'])

    item15 = "M&E above First Floor"
    segment = ''
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

    meAbovefirstFloorResults_dict = {"items": item15, "Segment": segment,
                                     "ifBuilding": ifBuilding, "ifContents": ifContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("meAbovefirstFloorResults_dict  : ", meAbovefirstFloorResults_dict)
    meAbovefirstFloorResults = riskrating2results(items=item15,
                                                  inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                  stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                  tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                  greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                  )
    meAbovefirstFloorResults.save()
    return [{"results": meAbovefirstFloorResults_dict}]


def coverageValue(inputs):
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
    segment = ''
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

    coverageValueFactorResults_dict = {"items": item16, "Segment": segment,
                                       "ifBuilding": ifBuilding, "ifContents": ifContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("coverageValueFactorResults_dict  : ", coverageValueFactorResults_dict)
    coverageValueFactorResults = riskrating2results(items=item16,
                                                    inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                    stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                    tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                    greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                    )
    coverageValueFactorResults.save()
    return [{"results": coverageValueFactorResults_dict}]


def CoverageValueRatio(inputs):
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
    segment = ''
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

    deductibleLimittoCoverageValueResults_dict = {"items": item17, "Segment": segment,
                                                  "ifBuilding": ifBuilding, "ifContents": ifContents,
                                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                  "glBuilding": glBuilding, "glContents": glContents,
                                                  "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("deductibleLimittoCoverageValueResults_dict  : ", deductibleLimittoCoverageValueResults_dict)
    deductibleLimittoCoverageValueResults = riskrating2results(items=item17,
                                                               inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                               coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                               )
    deductibleLimittoCoverageValueResults.save()

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
    segment = ''
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

    deductibletoCoverageValueResults_dict = {"items": item18, "Segment": segment,
                                             "ifBuilding": ifBuilding, "ifContents": ifContents,
                                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                             "glBuilding": glBuilding, "glContents": glContents,
                                             "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("deductibletoCoverageValueResults_dict  : ", deductibletoCoverageValueResults_dict)
    deductibletoCoverageValueResults = riskrating2results(items=item18,
                                                          inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                          coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                          )
    deductibletoCoverageValueResults.save()

    item19 = "Initial Deductible & ITV"
    segment = ''
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

    initialDeductibleITVResults_dict = {"items": item19, "Segment": segment,
                                        "ifBuilding": ifBuilding, "ifContents": ifContents,
                                        "ssBuilding": ssBuilding, "ssContents": ssContents,
                                        "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                        "glBuilding": glBuilding, "glContents": glContents,
                                        "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("initialDeductibleITVResults_dict  : ", initialDeductibleITVResults_dict)
    initialDeductibleITVResults = riskrating2results(items=item19,
                                                     inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                     stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                     tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                     greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                     coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                     )
    initialDeductibleITVResults.save()

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
        glContents = max(0.001, S_cont1int)
        ceContents = max(0.001, S_cont1int)
    finalDeductibleITVResults_dict = {"items": item20, "Segment": segment,
                                      "ifBuilding": ifBuilding, "ifContents": ifContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents}

    # print("finalDeductibleITVResults_dict  : ", finalDeductibleITVResults_dict)
    finalDeductibleITVResults = riskrating2results(items=item20,
                                                   inlandFloodBuldings=ifBuilding, inlandFloodContents=ifContents,
                                                   stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                   tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                   greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                   coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                   )
    finalDeductibleITVResults.save()
    return [{"deductibleLimittoCoverage results": deductibleLimittoCoverageValueResults_dict}, {"deductibletoCoverage results": deductibletoCoverageValueResults_dict}, {"initialDeductibleITV results": initialDeductibleITVResults_dict}, {"finalDeductibleITV results": finalDeductibleITVResults_dict}]


# #################Concentration Risk
#     conc_risk_mapping = pd.read_excel(path+"/tables/"+'Concentration Risk Mapping'+ '.xlsx')
#     conc_risk_mapping = conc_risk_mapping[(conc_risk_mapping[conc_risk_mapping.columns[0]]== inputs['State (Long)']) & (conc_risk_mapping[conc_risk_mapping.columns[1]]== inputs['County'])]
#     msa = conc_risk_mapping.iloc[0][2]
#     conc_risk = pd.read_excel(path+"/tables/"+'Concentration Risk'+ '.xlsx')
#     conc_risk = conc_risk[(conc_risk[conc_risk.columns[0]]== msa)]
            
#     risk_rating_2.iloc[22,1] = float(conc_risk[conc_risk.columns[2]])
#     risk_rating_2.iloc[22,2] = float(conc_risk[conc_risk.columns[2]])
#     risk_rating_2.iloc[22,3] = float(conc_risk[conc_risk.columns[3]])
#     risk_rating_2.iloc[22,4] = float(conc_risk[conc_risk.columns[3]])
#     ##########CRS disc
#     risk_rating_2.iloc[23][1:] = float(inputs['CRS discount']/100)
#     risk_rating_2.iloc[24][1:] = 1-float(inputs['CRS discount']/100)
#     #########
#     x= 1
#     for i in range(1,11):
#         risk_rating = risk_rating_2[risk_rating_2.columns[i]]
#         for j in range(0,11):   
#             y = risk_rating.iloc[j]
#             if str(y)!= 'nan':
#                 x*=y
#         risk_rating_2.iloc[11,i] = round(x,4)
#         x = 1      
#     x= 1
#     for i in range(1,11):
#         risk_rating = risk_rating_2[risk_rating_2.columns[i]]
#         for j in range(11,18):   
#             y = risk_rating.iloc[j]
#             if str(y)!= 'nan':
#                 x*=y
#         risk_rating_2.iloc[25,i] = round(x,4)
#         x = 1      
    
#     risk_rating_2.iloc[25][1:-1] =  (risk_rating_2.iloc[21][1:-1] * risk_rating_2.iloc[24][1:-1] * risk_rating_2.iloc[25][1:-1])
#     risk_rating_2.iloc[25,1] = risk_rating_2.iloc[25,1] *risk_rating_2.iloc[22,1] 
#     risk_rating_2.iloc[25,2] = risk_rating_2.iloc[25,2] *risk_rating_2.iloc[22,2] 
#     risk_rating_2.iloc[25,3] = risk_rating_2.iloc[25,3] *risk_rating_2.iloc[22,3] 
#     risk_rating_2.iloc[25,4] = risk_rating_2.iloc[25,4] *risk_rating_2.iloc[22,4] 
#     ##########################
#     Rate_of_building = round(( risk_rating_2.iloc[25,1] +
#                         risk_rating_2.iloc[25,3] +
#                         risk_rating_2.iloc[25,5] +
#                         risk_rating_2.iloc[25,7] +
#                         risk_rating_2.iloc[25,9] ),4)
    
#     Rate_of_contents = round(( risk_rating_2.iloc[25,2] +
#                         risk_rating_2.iloc[25,4] +
#                         risk_rating_2.iloc[25,6] +
#                         risk_rating_2.iloc[25,8] +
#                         risk_rating_2.iloc[25,10] ),4)
    
#     risk_rating_2.iloc[26,11] = Rate_of_building
#     risk_rating_2.iloc[27,11] = Rate_of_contents

#     risk_rating_2.iloc[28,1] = round((risk_rating_2.iloc[25,1]/ Rate_of_building )*100,4)
#     risk_rating_2.iloc[28,3] = round((risk_rating_2.iloc[25,3]/ Rate_of_building)*100,4)
#     risk_rating_2.iloc[28,5] = round((risk_rating_2.iloc[25,5]/ Rate_of_building)*100,4)
#     risk_rating_2.iloc[28,7] = round((risk_rating_2.iloc[25,7]/ Rate_of_building)*100,4)
#     risk_rating_2.iloc[28,9] = round((risk_rating_2.iloc[25,9]/ Rate_of_building)*100,4)
#     risk_rating_2.iloc[28,2] = round((risk_rating_2.iloc[25,2]/ Rate_of_contents)*100,4)
#     risk_rating_2.iloc[28,4] = round((risk_rating_2.iloc[25,4]/ Rate_of_contents)*100,4)
#     risk_rating_2.iloc[28,6] = round((risk_rating_2.iloc[25,6]/ Rate_of_contents)*100,4)
#     risk_rating_2.iloc[28,8] = round((risk_rating_2.iloc[25,8]/ Rate_of_contents)*100,4)
#     risk_rating_2.iloc[28,10] = round((risk_rating_2.iloc[25,10]/ Rate_of_contents)*100,4)
#     ######################
#     weighted_deductible_building =  round((risk_rating_2.iloc[21,1] * risk_rating_2.iloc[28,1]+
#                                     risk_rating_2.iloc[21,3] * risk_rating_2.iloc[28,3]+
#                                     risk_rating_2.iloc[21,5] * risk_rating_2.iloc[28,5]+
#                                     risk_rating_2.iloc[21,7] * risk_rating_2.iloc[28,7]+
#                                     risk_rating_2.iloc[21,9] * risk_rating_2.iloc[28,9])/100,4)
    
    
#     weighted_deductible_contents =  round((risk_rating_2.iloc[21,2] * risk_rating_2.iloc[28,2]+
#                                     risk_rating_2.iloc[21,4] * risk_rating_2.iloc[28,4]+
#                                     risk_rating_2.iloc[21,6] * risk_rating_2.iloc[28,6]+
#                                     risk_rating_2.iloc[21,8] * risk_rating_2.iloc[28,8]+
#                                     risk_rating_2.iloc[21,10] * risk_rating_2.iloc[28,10])/100,4)
    
#     min_rate_building = round(0 * weighted_deductible_building,4)
#     max_rate_building = round(15 * weighted_deductible_building,4)  
#     min_rate_contents = round(0 * weighted_deductible_contents,4)
#     max_rate_contents = round(15 * weighted_deductible_contents,4)  
#     final_rate_building = min(max(Rate_of_building,min_rate_building),max_rate_building ) 
#     final_rate_contents =  min(max(Rate_of_contents,min_rate_contents),max_rate_contents ) 
    
#     risk_rating_2.iloc[29,11] = weighted_deductible_building
#     risk_rating_2.iloc[30,11] = weighted_deductible_contents
#     risk_rating_2.iloc[31,11] = min_rate_building
#     risk_rating_2.iloc[32,11] = max_rate_building
#     risk_rating_2.iloc[33,11] = min_rate_contents
#     risk_rating_2.iloc[34,11] = max_rate_contents
#     risk_rating_2.iloc[37,11] = final_rate_building
#     risk_rating_2.iloc[38,11] = final_rate_contents
    
#     coverage_building_thousands = inputs['Coverage A value']/1000 
#     coverage_contents_thousands = inputs['Coverage C value']/1000 
#     initial_premium_without_fees_building = final_rate_building * coverage_building_thousands
#     initial_premium_without_fees_contents = final_rate_contents * coverage_contents_thousands
#     initial_premium_without_fees = initial_premium_without_fees_building + initial_premium_without_fees_contents 
#     prior_claim_premium = (inputs['Prior Claim Rate'] * coverage_building_thousands * weighted_deductible_building * max(0,inputs['Prior claims']-1))
#     premium_exc_fees_expense = initial_premium_without_fees + prior_claim_premium
#     premium_without_fees = premium_exc_fees_expense + inputs['Loss Constant']  + inputs['Expense Constant'] 
#     icc_crs = inputs['ICC premium'] * (100-inputs['CRS discount'])/100
#     subtotal = (premium_without_fees + icc_crs)
    
#     risk_rating_2.iloc[39,11] = coverage_building_thousands
#     risk_rating_2.iloc[40,11] = coverage_contents_thousands
#     risk_rating_2.iloc[41,11] = initial_premium_without_fees_building
#     risk_rating_2.iloc[42,11] = initial_premium_without_fees_contents
#     risk_rating_2.iloc[43,11] = initial_premium_without_fees
#     risk_rating_2.iloc[44,11] = prior_claim_premium
#     risk_rating_2.iloc[45,11] = premium_exc_fees_expense
#     risk_rating_2.iloc[46,11] = inputs['Expense Constant'] 
#     risk_rating_2.iloc[47,11] = inputs['Loss Constant']
#     risk_rating_2.iloc[48,11] = premium_without_fees
#     risk_rating_2.iloc[49,11] = inputs['ICC premium']
#     risk_rating_2.iloc[50,11] = icc_crs
#     risk_rating_2.iloc[51,11] = subtotal
#     risk_rating_2.iloc[52,11] = inputs['Reserve fund']

#     subtotal = subtotal * inputs['Reserve fund']
#     risk_rating_2.iloc[53,11] = subtotal
#     risk_rating_2.iloc[54,11] = inputs['Probation surcharge']
    
#     if inputs['Primary residence indicator'] == 'Yes':
#         HFIAA_surcharge = 50    
#     else:
#         HFIAA_surcharge = 250    
#     risk_rating_2.iloc[55,11] = HFIAA_surcharge
#     risk_rating_2.iloc[56,11] = inputs['Federal policy fee']  
#     premium = round(subtotal + inputs['Probation surcharge'] + HFIAA_surcharge + inputs['Federal policy fee']  ,2)
#     risk_rating_2.iloc[57,11] = premium
#     return risk_rating_2



