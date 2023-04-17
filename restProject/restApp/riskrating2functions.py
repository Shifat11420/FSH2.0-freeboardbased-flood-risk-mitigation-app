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
    ceBuilding = floorsOfInt_allexclCE[0]
    ceContents = floorsOfInt_allexclCE[0]

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
    ceBuilding = foundation_allexclCE[0]
    ceContents = foundation_allexclCE[0]

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
