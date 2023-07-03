from .models import *
from rest_framework.response import Response
import pandas as pd
import numpy as np
from django.db.models import Q


def RRFunctionsLevee(inputs, currentScenario):
    # Base Rate
    baserate = baseRateMultipliers.objects.filter(levee="Yes",
                                                  region=currentScenario.state, singleFamilyHomeIndicator=currentScenario.typeOfUseID.singleFamilyHomeIndicatorID).all()

    item1 = "Base Rate (per $1000 of Coverage Value)"
    ifFluvialBuilding = baserate.filter(
        ifType='Fluvial').values()[0]['ifBuilding']
    ifFluvialContents = baserate.filter(
        ifType='Fluvial').values()[0]['ifContents']
    ifPluvialBuilding = baserate.filter(
        ifType='Pluvial').values()[0]['ifBuilding']
    ifPluvialContents = baserate.filter(
        ifType='Pluvial').values()[0]['ifContents']
    ssBuilding = baserate.values()[0]['ssBuilding']
    ssContents = baserate.values()[0]['ssContents']
    tsuBuilding = baserate.values()[0]['tsuBuilding']
    tsuContents = baserate.values()[0]['tsuContents']
    glBuilding = baserate.values()[0]['glBuilding']
    glContents = baserate.values()[0]['glContents']
    ceBuilding = baserate.values()[0]['ceBuilding']
    ceContents = baserate.values()[0]['ceContents']
    allPerils = ''

    baserateResults_dict = {"items": item1,
                            "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                            "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}
    # print("baserate Results  : ", baserateResults_dict)

    baseRateResult = riskrating2resultsLevee(items=item1,
                                             inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                             inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                             stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                             tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                             greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                             coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                             )
    baseRateResult.save()

    # Distance To River
    disttoriver = distToRiverMultipliers.objects.filter(levee="Yes").all()

    dtrMetersFluvial = disttoriver.filter(
        ifType='Fluvial').values_list("dtr_meters", flat=True)
    dtrMetersFluvial = list(dtrMetersFluvial)
    dtrMetersPluvial = disttoriver.filter(
        ifType='Pluvial').values_list("dtr_meters", flat=True)
    dtrMetersPluvial = list(dtrMetersPluvial)

    ifvalueBFluvial = disttoriver.filter(
        ifType='Fluvial').values_list("ifvalue", flat=True)
    ifvalueBFluvial = list(ifvalueBFluvial)
    ifvalueBPluvial = disttoriver.filter(
        ifType='Pluvial').values_list("ifvalue", flat=True)
    ifvalueBPluvial = list(ifvalueBPluvial)

    if currentScenario.distToRiver != None and currentScenario.distToRiver <= 1700:
        B1 = np.interp([currentScenario.distToRiver], dtrMetersFluvial,
                       ifvalueBFluvial)
        B2 = np.interp([currentScenario.distToRiver], dtrMetersPluvial,
                       ifvalueBPluvial)

    item2 = "Distance to River"
    ifFluvialBuilding = round(float(B1), 4)
    ifFluvialContents = round(float(B1), 4)
    ifPluvialBuilding = round(float(B2), 4)
    ifPluvialContents = round(float(B2), 4)
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
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("distToRiver Results  : ", distToRiverResults_dict)
    distToRiverResult = riskrating2resultsLevee(items=item2,
                                                inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents)
    distToRiverResult.save()

    # Elevation Relative To River
    elevRiver = elevRelToRiver.objects.filter(levee="Yes",
                                              riverClass='Class '+str(currentScenario.riverClass)).all()

    err_feetFluvial = elevRiver.filter(
        ifType='Fluvial').values_list("err_feet", flat=True)
    err_feetFluvial = list(err_feetFluvial)
    err_feetPluvial = elevRiver.filter(
        ifType='Pluvial').values_list("err_feet", flat=True)
    err_feetPluvial = list(err_feetPluvial)

    ifvalueCFluvial = elevRiver.filter(
        ifType='Fluvial').values_list("ifvalue", flat=True)
    ifvalueCFluvial = list(ifvalueCFluvial)
    ifvalueCPluvial = elevRiver.filter(
        ifType='Pluvial').values_list("ifvalue", flat=True)
    ifvalueCPluvial = list(ifvalueCPluvial)

    if currentScenario.elevRelToRiver == None:  # 'N/A':
        C1 = -9999.0  # np.nan
        C2 = -9999.0  # np.nan
    else:
        C1 = np.interp([currentScenario.elevRelToRiver], err_feetFluvial,
                       ifvalueCFluvial)
        C2 = np.interp([currentScenario.elevRelToRiver], err_feetPluvial,
                       ifvalueCPluvial)

    item3 = "Elevation Relative to River by River Class"
    ifFluvialBuilding = round(float(C1), 4)
    ifFluvialContents = round(float(C1), 4)
    ifPluvialBuilding = round(float(C2), 4)
    ifPluvialContents = round(float(C2), 4)
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
                                  "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                  "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                  "glBuilding": glBuilding, "glContents": glContents,
                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                  "allPerils": allPerils}

    # print("elevRelToRiverResults_dict  : ", elevRelToRiverResults_dict)
    elevRelToRiverResults = riskrating2resultsLevee(items=item3,
                                                    inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                    inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents)
    elevRelToRiverResults.save()

    # Drainage Area
    D = 1.0
    item4 = "Drainage Area"
    ifFluvialBuilding = round(float(D), 4)
    ifFluvialContents = round(float(D), 4)
    ifPluvialBuilding = round(float(D), 4)
    ifPluvialContents = round(float(D), 4)
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
                                "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                "glBuilding": glBuilding, "glContents": glContents,
                                "ceBuilding": ceBuilding, "ceContents": ceContents,
                                "allPerils": allPerils}

    # print("drainageAreaResults_dict  : ", drainageAreaResults_dict)
    drainageAreaResults = riskrating2resultsLevee(items=item4,
                                                  inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                  inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents)
    drainageAreaResults.save()

    # Strucral Relative Elevation
    strucRelElv = structuralRelElevation.objects.filter(levee="Yes").all()

    sre_feetFluvial = strucRelElv.filter(
        ifType='Fluvial').values_list("sre_feet", flat=True)
    sre_feetFluvial = list(sre_feetFluvial)
    sre_feetPluvial = strucRelElv.filter(
        ifType='Pluvial').values_list("sre_feet", flat=True)
    sre_feetPluvial = list(sre_feetPluvial)
    ifvalueEFluvial = strucRelElv.filter(
        ifType='Fluvial').values_list("ifvalue", flat=True)
    ifvalueEFluvial = list(ifvalueEFluvial)
    ifvalueEPluvial = strucRelElv.filter(
        ifType='Pluvial').values_list("ifvalue", flat=True)
    ifvalueEPluvial = list(ifvalueEPluvial)

    E1 = np.interp([currentScenario.strRelElev],
                   sre_feetFluvial, ifvalueEFluvial)
    E2 = np.interp([currentScenario.strRelElev],
                   sre_feetPluvial, ifvalueEPluvial)

    item5 = "Structural Relative Elevation"
    ifFluvialBuilding = round(float(E1), 4)
    ifFluvialContents = round(float(E1), 4)
    ifPluvialBuilding = round(float(E2), 4)
    ifPluvialContents = round(float(E2), 4)
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
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("strucRelElvResults_dict  : ", strucRelElvResults_dict)
    strucRelElvResults = riskrating2resultsLevee(items=item5,
                                                 inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                 inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents)
    strucRelElvResults.save()

    # Distance To Coast
    distToCoast = distToCoastMultipliers.objects.filter(levee="Yes").all()

    dtc_meters = distToCoast.filter(
        ~Q(ce=-9999.0)).values_list("dtc_meters", flat=True)
    dtc_meters = list(dtc_meters)
    ce = distToCoast.filter(
        ~Q(ce=-9999.0)).values_list("ce", flat=True)
    ce = list(ce)

    if currentScenario.distToCoast == None:
        coast = -9999.0  # np.nan
    else:
        coast = np.interp([currentScenario.distToCoast], dtc_meters, ce)

    if currentScenario.distToCoast != None:
        dtc_others = distToCoastMultipliers.objects.filter(levee="Yes").all()
        if currentScenario.state != "LA":
            dtc_others = dtc_others.filter(region='Non-LA').all()
        else:
            dtc_others = dtc_others.filter(
                region=currentScenario.state).all()

        dtc_meters_ss = dtc_others.filter(
            ~Q(ss=-9999.0)).values_list("dtc_meters", flat=True)
        dtc_meters_ss = list(dtc_meters_ss)

        dtc_meters_tsu = dtc_others.filter(region=currentScenario.state).filter(
            ~Q(tsu=-9999.0)).values_list("dtc_meters", flat=True)
        dtc_meters_tsu = list(dtc_meters_tsu)

        if len(dtc_meters_ss) != 0:
            ss = dtc_others.filter(
                ~Q(ss=-9999.0)).values_list("ss", flat=True)
            ss = list(ss)
            storm = np.interp([currentScenario.distToCoast], dtc_meters_ss, ss)
        else:
            storm = -9999.0  # np.nan

        if len(dtc_meters_tsu) != 0:
            tsu = dtc_others.filter(
                ~Q(tsu=-9999.0)).values_list("tsu", flat=True)
            tsu = list(tsu)
            tsunami = np.interp(
                [currentScenario.distToCoast], dtc_meters_tsu, tsu)
        else:
            tsunami = -9999.0  # np.nan
    else:
        storm = -9999.0  # np.nan
        tsunami = -9999.0  # np.nan

    item6 = "Distance to Coast"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
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
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("distToCoastResults_dict  : ", distToCoastResults_dict)
    distToCoastResults = riskrating2resultsLevee(items=item6,
                                                 stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                 tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                 coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents)
    distToCoastResults.save()

    # Distance To Ocean
    if currentScenario.distToOcean != None:
        dto = distToOceanMultipliers.objects.filter(levee="Yes",
                                                    region=currentScenario.state).all()
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

        if len(dto_ss) != 0:
            storm = np.interp([currentScenario.distToOcean], dto_ss, ss)
        else:
            storm = -9999.0  # np.nan

        if len(dto_tsu) != 0:
            tsunami = np.interp([currentScenario.distToOcean], dto_tsu, tsu)
        else:
            tsunami = -9999.0  # np.nan
    else:
        storm = -9999.0  # np.nan
        tsunami = -9999.0  # np.nan

    item7 = "Distance to Ocean"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
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
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
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
    if currentScenario.state != "LA":
        # if inputs['State'] == "Non-LA":
        elev = elevation.objects.filter(levee="Yes",
                                        region="Non-LA").all()
    else:
        elev = elevation.objects.filter(levee="Yes",
                                        region=currentScenario.state).all()

    elev_ifF = elev.filter(
        ifType='Fluvial').filter(
        ~Q(ifvalue=-9999.0)).values_list("elevation_feet", flat=True)
    elev_ifF = list(elev_ifF)

    elev_ifP = elev.filter(
        ifType='Pluvial').filter(
        ~Q(ifvalue=-9999.0)).values_list("elevation_feet", flat=True)
    elev_ifP = list(elev_ifP)

    elev_ss = elev.filter(
        ~Q(ss=-9999.0)).values_list("elevation_feet", flat=True)
    elev_ss = list(elev_ss)
    elev_tsu = elev.filter(
        ~Q(tsu=-9999.0)).values_list("elevation_feet", flat=True)
    elev_tsu = list(elev_tsu)
    iff = elev.filter(
        ifType='Fluvial').filter(
        ~Q(ifvalue=-9999.0)).values_list("ifvalue", flat=True)
    iff = list(iff)
    ifp = elev.filter(
        ifType='Pluvial').filter(
        ~Q(ifvalue=-9999.0)).values_list("ifvalue", flat=True)
    ifp = list(ifp)
    ss = elev.filter(
        ~Q(ss=-9999.0)).values_list("ss", flat=True)
    ss = list(ss)
    tsu = elev.filter(
        ~Q(tsu=-9999.0)).values_list("tsu", flat=True)
    tsu = list(tsu)

    if len(elev_ifF) != 0:
        ifFluvial = np.interp([currentScenario.elevation], elev_ifF, iff)
    else:
        ifFluvial = -9999.0  # np.nan

    if len(elev_ifP) != 0:
        ifPluvial = np.interp([currentScenario.elevation], elev_ifP, ifp)
    else:
        ifPluvial = -9999.0  # np.nan

    if len(elev_ss) != 0:
        storm = np.interp([currentScenario.elevation], elev_ss, ss)
    else:
        storm = -9999.0  # np.nan

    if len(elev_tsu) != 0:
        tsunami = np.interp([currentScenario.elevation], elev_tsu, tsu)
    else:
        tsunami = -9999.0  # np.nan

    item8 = "Elevation"
    ifFluvialBuilding = round(float(ifFluvial), 4)
    ifFluvialContents = round(float(ifFluvial), 4)
    ifPluvialBuilding = round(float(ifPluvial), 4)
    ifPluvialContents = round(float(ifPluvial), 4)
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
                             "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                             "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("elevationResults_dict  : ", elevationResults_dict)
    elevationResults = riskrating2resultsLevee(items=item8,
                                               inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                               inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents
                                               )
    elevationResults.save()

    # Distance To Lake
    dist_lake = distToLakeMultipliers.objects.filter(levee="Yes").all()

    if currentScenario.distToLake == None:
        greatlakesbuilding = 0.525
        greatlakescontent = 0.525
    else:
        dtl_meters = dist_lake.filter(
            ~Q(gl=-9999.0)).values_list("dtl_meters", flat=True)
        dtl_meters = list(dtl_meters)
        gl = dist_lake.filter(
            ~Q(gl=-9999.0)).values_list("gl", flat=True)
        gl = list(gl)

        I = np.interp([currentScenario.distToLake], dtl_meters, gl)
        greatlakesbuilding = round(float(I), 4)
        greatlakescontent = round(float(I), 4)

    item9 = "Distance to Lake"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
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
                              "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                              "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents,
                              "allPerils": allPerils}

    # print("disttolakeResults_dict  : ", disttolakeResults_dict)
    disttolakeResults = riskrating2resultsLevee(items=item9,
                                                greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                )
    disttolakeResults.save()

    # Elevation Relative To Lake
    elev_lake = elevRelToLake.objects.filter(levee="Yes").all()

    if currentScenario.distToLake == None:
        greatlakesbuilding = 0.004
        greatlakescontent = 0.004
    else:
        erl_feet = elev_lake.filter(
            ~Q(gl=-9999.0)).values_list("erl_feet", flat=True)
        erl_feet = list(erl_feet)
        gl = elev_lake.filter(
            ~Q(gl=-9999.0)).values_list("gl", flat=True)
        gl = list(gl)

        J = np.interp([currentScenario.elevRelToLake], erl_feet, gl)
        greatlakesbuilding = round(float(J), 4)
        greatlakescontent = round(float(J), 4)

    item10 = "Elevation Relative to Lake"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
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
                                      "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                      "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}

    # print("elevationRelToLakeResults_dict  : ", elevationRelToLakeResults_dict)
    elevationRelToLakeResults = riskrating2resultsLevee(items=item10,
                                                        greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                        )
    elevationRelToLakeResults.save()

    levee_qual = leveeQuality.objects.filter(leveeSystemID=int(
        currentScenario.leveeID)).all()
    iff = levee_qual.values_list("leveeQualityFactor", flat=True)
    iff = list(iff)

    item11 = "Levee Quality"
    ifFluvialBuilding = round(float(iff[0]), 4)
    ifFluvialContents = round(float(iff[0]), 4)
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    leveeQualityResults_dict = {"items": item11,
                                "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                "glBuilding": glBuilding, "glContents": glContents,
                                "ceBuilding": ceBuilding, "ceContents": ceContents,
                                "allPerils": allPerils}

    # print("territoryResults_dict  : ", leveeQualityResults_dict)
    leveeQualityResults = riskrating2resultsLevee(items=item11,
                                                  inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,)
    leveeQualityResults.save()

    # # Territory
    # # TSU
    territory_huc12_tsu = territory.objects.filter(levee="Yes",
                                                   huc12=int(currentScenario.HUC12), peril='Tsu').all()

    if territory_huc12_tsu.count() == 0:
        tsuBldg = -9999.0
        tsuCont = -9999.0
    else:
        territory_tsu = territory_huc12_tsu.filter(
            ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
        territory_tsu = list(territory_tsu)
        tsuBldg = round(territory_tsu[0], 4)
        tsuCont = round(territory_tsu[0], 4)

    # # GL
    territory_huc12_gl = territory.objects.filter(levee="Yes",
                                                  huc12=int(currentScenario.HUC12), peril='GL').all()

    if territory_huc12_gl.count() == 0:
        glBldg = -9999.0
        glCont = -9999.0
    else:
        territory_gl = territory_huc12_gl.filter(
            ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
        territory_gl = list(territory_gl)
        glBldg = round(territory_gl[0], 4)
        glCont = round(territory_gl[0], 4)

    # # IF
    territory_huc12_if = territory.objects.filter(levee="Yes", leveeSystemID=int(
        currentScenario.leveeID), huc12=int(currentScenario.HUC12), peril='IF').all()

    territory_if = territory_huc12_if.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_if = list(territory_if)
    ifBldg = round(territory_if[0], 4)
    ifCont = round(territory_if[0], 4)

    # SS
    territory_huc12_ss = territory.objects.filter(levee="Yes",
                                                  huc12=int(currentScenario.HUC12), leveeSystemID=int(currentScenario.leveeID), peril='SS').all()

    territory_ss = territory_huc12_ss.filter(
        ~Q(ratingFactors=-9999.0)).values_list("ratingFactors", flat=True)
    territory_ss = list(territory_ss)
    ssBldg = round(territory_ss[0], 4)
    ssCont = round(territory_ss[0], 4)

    item12 = "Territory (HUC12 & Barrier Island Indicator)"
    ifFluvialBuilding = ifBldg
    ifFluvialContents = ifCont
    ifPluvialBuilding = ifBldg
    ifPluvialContents = ifCont
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
                             "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                             "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("territoryResults_dict  : ", territoryResults_dict)
    territoryResults = riskrating2resultsLevee(items=item12,
                                               inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                               inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                               )
    territoryResults.save()

    # Type Of Use
    typeuse = typeOfUse.objects.filter(
        typeofuse=currentScenario.typeOfUseID).all()

    typeuse_if = typeuse.values_list('flood', flat=True)
    typeuse_if = list(typeuse_if)
    typeuse_ss = typeuse.values_list('surge', flat=True)
    typeuse_ss = list(typeuse_ss)
    typeuse_tsu = typeuse.values_list('tsunami', flat=True)
    typeuse_tsu = list(typeuse_tsu)
    typeuse_gl = typeuse.values_list('lakes', flat=True)
    typeuse_gl = list(typeuse_gl)

    item13 = "Type of Use"
    ifFluvialBuilding = typeuse_if[0]
    ifFluvialContents = typeuse_if[0]
    ifPluvialBuilding = typeuse_if[0]
    ifPluvialContents = typeuse_if[0]
    ssBuilding = typeuse_ss[0]
    ssContents = typeuse_ss[0]
    tsuBuilding = typeuse_tsu[0]
    tsuContents = typeuse_tsu[0]
    glBuilding = typeuse_gl[0]
    glContents = typeuse_gl[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    typeOfUseResults_dict = {"items": item13,
                             "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                             "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                             "glBuilding": glBuilding, "glContents": glContents,
                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                             "allPerils": allPerils}

    # print("typeOfUseResults_dict  : ", typeOfUseResults_dict)
    typeOfUseResults = riskrating2resultsLevee(items=item13,
                                               inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                               inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                               )
    typeOfUseResults.save()

    # Floors Of Interest
    floorsOfInt = floorsOfInterest.objects.filter(
        homeIndicator=currentScenario.typeOfUseID.singleFamilyHomeIndicatorID, ownerIndicator=currentScenario.typeOfUseID.condoUnitOwnerIndicatorID, interest=currentScenario.floorID).all()

    floorsOfInt_allexclCE = floorsOfInt.values_list('allExclCE', flat=True)
    floorsOfInt_allexclCE = list(floorsOfInt_allexclCE)

    item14 = "Floor of Interest"
    ifFluvialBuilding = floorsOfInt_allexclCE[0]
    ifFluvialContents = floorsOfInt_allexclCE[0]
    ifPluvialBuilding = floorsOfInt_allexclCE[0]
    ifPluvialContents = floorsOfInt_allexclCE[0]
    ssBuilding = floorsOfInt_allexclCE[0]
    ssContents = floorsOfInt_allexclCE[0]
    tsuBuilding = floorsOfInt_allexclCE[0]
    tsuContents = floorsOfInt_allexclCE[0]
    glBuilding = floorsOfInt_allexclCE[0]
    glContents = floorsOfInt_allexclCE[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    floorsOfIntResults_dict = {"items": item14,
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("floorsOfIntResults_dict  : ", floorsOfIntResults_dict)
    floorsOfIntResults = riskrating2resultsLevee(items=item14,
                                                 inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                 inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                 stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                 tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                 greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                 )
    floorsOfIntResults.save()

    # Foundation type
    foundation = foundationType.objects.filter(
        foundationtypes=currentScenario.foundationTypeID).all()

    foundation_allexclCE = foundation.values_list('allExclCE', flat=True)
    foundation_allexclCE = list(foundation_allexclCE)

    item15 = "Foundation Type"
    ifFluvialBuilding = foundation_allexclCE[0]
    ifFluvialContents = foundation_allexclCE[0]
    ifPluvialBuilding = foundation_allexclCE[0]
    ifPluvialContents = foundation_allexclCE[0]
    ssBuilding = foundation_allexclCE[0]
    ssContents = foundation_allexclCE[0]
    tsuBuilding = foundation_allexclCE[0]
    tsuContents = foundation_allexclCE[0]
    glBuilding = foundation_allexclCE[0]
    glContents = foundation_allexclCE[0]
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    foundationResults_dict = {"items": item15,
                              "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                              "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                              "ssBuilding": ssBuilding, "ssContents": ssContents,
                              "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                              "glBuilding": glBuilding, "glContents": glContents,
                              "ceBuilding": ceBuilding, "ceContents": ceContents,
                              "allPerils": allPerils}

    # print("foundationResults_dict  : ", foundationResults_dict)
    foundationResults = riskrating2resultsLevee(items=item15,
                                                inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
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

    if str(currentScenario.foundationTypeID.foundationDesignforType) == "Open, No Obstruction":
        floodEventyesWFV = fffvOpenNoObsWFV
        floodEventnoWbyFV = fffvOpenNoObsWbyFV
    elif str(currentScenario.foundationTypeID.foundationDesignforType) == "Open, Obstruction":
        floodEventyesWFV = fffvOpenObsWFV
        floodEventnoWbyFV = fffvOpenObsWbyFV
    elif str(currentScenario.foundationTypeID.foundationDesignforType) == "Closed, Wall":
        floodEventyesWFV = fffvClosedWallWFV
        floodEventnoWbyFV = fffvClosedWallWbyFV

    # floodEventnoWbyFV = fffvOpenNoObsWbyFV  # testing purpose, to be excluded
    if str(currentScenario.floodVentsID) == "Yes":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventyesWFV)
    elif str(currentScenario.floodVentsID) == "No":
        P = np.interp([inputs['First floor height']],
                      fffvHeight, floodEventnoWbyFV)
    # print("fffvHeight = ")
    # print(fffvHeight)
    # print("floodEventnoWbyFV = ")
    # print(floodEventnoWbyFV)
    # print("First_floor_foundation_vent = ", P)

    P = round(float(P), 4)

    item16 = "First Floor Height by Foundation Design & Flood Vents"
    ifFluvialBuilding = P
    ifFluvialContents = P
    ifPluvialBuilding = P
    ifPluvialContents = P
    ssBuilding = P
    ssContents = P
    tsuBuilding = P
    tsuContents = P
    glBuilding = P
    glContents = P
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    firstFloorHeightResults_dict = {"items": item16,
                                    "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                    "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                    "ssBuilding": ssBuilding, "ssContents": ssContents,
                                    "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                    "glBuilding": glBuilding, "glContents": glContents,
                                    "ceBuilding": ceBuilding, "ceContents": ceContents,
                                    "allPerils": allPerils}

    # print("firstFloorHeightResults_dict  : ", firstFloorHeightResults_dict)
    firstFloorHeightResults = riskrating2resultsLevee(items=item16,
                                                      inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                      inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                      stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                      tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                      greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                      )
    firstFloorHeightResults.save()

    # ME Above First Floor
    me = MEAboveFirstFloor.objects.filter(
        machineryEquipmentAboveFirstFloor=currentScenario.MandEID).all()

    meCE = float(me.values()[0]['coastalErosion'])

    item17 = "M&E above First Floor"
    ifFluvialBuilding = meCE
    ifFluvialContents = meCE
    ifPluvialBuilding = meCE
    ifPluvialContents = meCE
    ssBuilding = meCE
    ssContents = meCE
    tsuBuilding = meCE
    tsuContents = meCE
    glBuilding = meCE
    glContents = meCE
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    meAbovefirstFloorResults_dict = {"items": item17,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("meAbovefirstFloorResults_dict  : ", meAbovefirstFloorResults_dict)
    meAbovefirstFloorResults = riskrating2resultsLevee(items=item17,
                                                       inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                       inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
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

    build = np.interp([currentScenario.buildingValue], bldgValue_value,
                      bldgValue_allexclCE)
    content = np.interp([currentScenario.contentsValue], contValue_value,
                        contValue_allexclCE)

    item18 = "Coverage Value Factor"
    ifFluvialBuilding = round(float(build), 4)
    ifFluvialContents = round(float(content), 4)
    ifPluvialBuilding = round(float(build), 4)
    ifPluvialContents = round(float(content), 4)
    ssBuilding = round(float(build), 4)
    ssContents = round(float(content), 4)
    tsuBuilding = round(float(build), 4)
    tsuContents = round(float(content), 4)
    glBuilding = round(float(build), 4)
    glContents = round(float(content), 4)
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    coverageValueFactorResults_dict = {"items": item18,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("coverageValueFactorResults_dict  : ",
    #       coverageValueFactorResults_dict)
    coverageValueFactorResults = riskrating2resultsLevee(items=item18,
                                                         inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                         inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                         stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                         tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                         greatLakesBuldings=glBuilding, greatLakesContents=glContents
                                                         )
    coverageValueFactorResults.save()

    # Deductible & Limit to Coverage Value Ratio
    deductible_limit_coverage_A = deductibleLimitITVCovA.objects.all()
    deductible_limit_coverage_C = deductibleLimitITVCovC.objects.all()

    ratio_A = max(min((currentScenario.buildingDeductible +
                  currentScenario.buildingCoverage) / currentScenario.buildingValue, 1), 0)
    ratio_C = max(min((currentScenario.contentsDeductible +
                  currentScenario.contentsCoverage) / currentScenario.contentsValue, 1), 0)

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

    item19 = "Deductible & Limit to Coverage Value Ratio"
    ifFluvialBuilding = round(float(S_build1_limit), 4)
    ifFluvialContents = round(float(S_cont1_limit), 4)
    ifPluvialBuilding = round(float(S_build1_limit), 4)
    ifPluvialContents = round(float(S_cont1_limit), 4)
    ssBuilding = round(float(S_build2_limit), 4)
    ssContents = round(float(S_cont2_limit), 4)
    tsuBuilding = round(float(S_build2_limit), 4)
    tsuContents = round(float(S_cont2_limit), 4)
    glBuilding = round(float(S_build2_limit), 4)
    glContents = round(float(S_cont2_limit), 4)
    ceBuilding = round(float(S_build2_limit), 4)
    ceContents = round(float(S_cont2_limit), 4)
    allPerils = ''

    deductibleLimittoCoverageValueResults_dict = {"items": item19,
                                                  "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                  "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                  "glBuilding": glBuilding, "glContents": glContents,
                                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                  "allPerils": allPerils}

    # print("deductibleLimittoCoverageValueResults_dict  : ", deductibleLimittoCoverageValueResults_dict)
    deductibleLimittoCoverageValueResults = riskrating2resultsLevee(items=item19,
                                                                    inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                                    inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
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
        min((currentScenario.buildingDeductible) / currentScenario.buildingValue, 1), 0)
    ratio_C = max(
        min((currentScenario.contentsDeductible) / currentScenario.contentsValue, 1), 0)

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

    item20 = "Deductible to Coverage Value Ratio"
    ifFluvialBuilding = round(float(S_build1), 4)
    ifFluvialContents = round(float(S_cont1), 4)
    ifPluvialBuilding = round(float(S_build1), 4)
    ifPluvialContents = round(float(S_cont1), 4)
    ssBuilding = round(float(S_build2), 4)
    ssContents = round(float(S_cont2), 4)
    tsuBuilding = round(float(S_build2), 4)
    tsuContents = round(float(S_cont2), 4)
    glBuilding = round(float(S_build2), 4)
    glContents = round(float(S_cont2), 4)
    ceBuilding = round(float(S_build2), 4)
    ceContents = round(float(S_cont2), 4)
    allPerils = ''

    deductibletoCoverageValueResults_dict = {"items": item20,
                                             "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                             "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                             "glBuilding": glBuilding, "glContents": glContents,
                                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                                             "allPerils": allPerils}

    # print("deductibletoCoverageValueResults_dict  : ", deductibletoCoverageValueResults_dict)
    deductibletoCoverageValueResults = riskrating2resultsLevee(items=item20,
                                                               inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                               inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                               stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                               tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                               greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                               coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                               )
    deductibletoCoverageValueResults.save()

    # Initial Deductible & ITV
    item21 = "Initial Deductible & ITV"
    S_build1int = round(float(S_build1_limit-S_build1), 4)
    S_cont1int = round(float(S_cont1_limit-S_cont1), 4)
    S_build2int = round(float(S_build2_limit-S_build2), 4)
    S_cont2int = round(float(S_cont2_limit-S_cont2), 4)

    ifFluvialBuilding = S_build1int
    ifFluvialContents = S_cont1int
    ifPluvialBuilding = S_build1int
    ifPluvialContents = S_cont1int
    ssBuilding = S_build2int
    ssContents = S_cont2int
    tsuBuilding = S_build2int
    tsuContents = S_cont2int
    glBuilding = S_build2int
    glContents = S_cont2int
    ceBuilding = S_build2int
    ceContents = S_cont2int
    allPerils = ''

    initialDeductibleITVResults_dict = {"items": item21,
                                        "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                        "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                        "ssBuilding": ssBuilding, "ssContents": ssContents,
                                        "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                        "glBuilding": glBuilding, "glContents": glContents,
                                        "ceBuilding": ceBuilding, "ceContents": ceContents,
                                        "allPerils": allPerils}

    # print("initialDeductibleITVResults_dict  : ", initialDeductibleITVResults_dict)
    initialDeductibleITVResults = riskrating2resultsLevee(items=item21,
                                                          inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                          inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                          stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                          tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                          greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                          coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                          )
    initialDeductibleITVResults.save()

    # Final Deductible & ITV
    item22 = "Final Deductible & ITV"
    if currentScenario.buildingCoverage == 0:
        ifFluvialBuilding = 0
        ifPluvialBuilding = 0
        ssBuilding = 0
        tsuBuilding = 0
        glBuilding = 0
        ceBuilding = 0
    else:
        ifFluvialBuilding = max(0.001, S_build1int)
        ifPluvialBuilding = max(0.001, S_build1int)
        ssBuilding = max(0.001, S_build2int)
        tsuBuilding = max(0.001, S_build2int)
        glBuilding = max(0.001, S_build2int)
        ceBuilding = max(0.001, S_build2int)

    if currentScenario.buildingCoverage == 0:
        ifFluvialContents = 0
        ifPluvialContents = 0
        ssContents = 0
        tsuContents = 0
        glContents = 0
        ceContents = 0
    else:
        ifFluvialContents = max(0.001, S_cont1int)
        ifPluvialContents = max(0.001, S_cont1int)
        ssContents = max(0.001, S_cont2int)
        tsuContents = max(0.001, S_cont2int)
        glContents = max(0.001, S_cont2int)
        ceContents = max(0.001, S_cont2int)
    allPerils = ''

    finalDeductibleITVResults_dict = {"items": item22,
                                      "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                      "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}
    # print("finalDeductibleITVResults_dict  : ", finalDeductibleITVResults_dict)
    finalDeductibleITVResults = riskrating2resultsLevee(items=item22,
                                                        inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                        inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                        stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                        tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                        greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                        coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents
                                                        )
    finalDeductibleITVResults.save()

    # Concentration Risk
    conc_risk_mapping = concentrationRiskMapping.objects.filter(
        state=currentScenario.stateLongName, county=currentScenario.county).all()
    msa = conc_risk_mapping.values()[0]['concentrationRiskTerritory']

    conc_risk = concentrationRisk.objects.filter(
        MSA=msa).all()

    item23 = "Concentration Risk"
    ifFluvialBuilding = conc_risk.values()[0]['flood']
    ifFluvialContents = conc_risk.values()[0]['flood']
    ifPluvialBuilding = conc_risk.values()[0]['flood']
    ifPluvialContents = conc_risk.values()[0]['flood']
    ssBuilding = conc_risk.values()[0]['surge']
    ssContents = conc_risk.values()[0]['surge']
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    concRiskResults_dict = {"items": item23,
                            "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                            "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}

    # print("concRiskResults_dict  : ", concRiskResults_dict)
    concRiskResults = riskrating2resultsLevee(items=item23,
                                              inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                              inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                              stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                              )
    concRiskResults.save()

    # CRS Discount Percentage
    CRSDiscountPercentage = float(currentScenario.crsRating.Value/100)
    item24 = "CRS Discount Percentage"
    ifFluvialBuilding = CRSDiscountPercentage
    ifFluvialContents = CRSDiscountPercentage
    ifPluvialBuilding = CRSDiscountPercentage
    ifPluvialContents = CRSDiscountPercentage
    ssBuilding = CRSDiscountPercentage
    ssContents = CRSDiscountPercentage
    tsuBuilding = CRSDiscountPercentage
    tsuContents = CRSDiscountPercentage
    glBuilding = CRSDiscountPercentage
    glContents = CRSDiscountPercentage
    ceBuilding = CRSDiscountPercentage
    ceContents = CRSDiscountPercentage
    allPerils = CRSDiscountPercentage

    CRSDiscountPercResults_dict = {"items": item24,
                                   "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                   "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                   "ssBuilding": ssBuilding, "ssContents": ssContents,
                                   "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                   "glBuilding": glBuilding, "glContents": glContents,
                                   "ceBuilding": ceBuilding, "ceContents": ceContents,
                                   "allPerils": allPerils}

    # print("CRSDiscountPercResults_dict  : ", CRSDiscountPercResults_dict)
    CRSDiscountPercResults = riskrating2resultsLevee(items=item24,
                                                     inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                     inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                     stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                     tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                     greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                     coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                     allPerilsAllCoverage=allPerils)
    CRSDiscountPercResults.save()

    # CRS Discount Factor
    CRSDiscountFactor = 1-float(currentScenario.crsRating.Value/100)
    item25 = "CRS Discount Factor"
    ifFluvialBuilding = CRSDiscountFactor
    ifFluvialContents = CRSDiscountFactor
    ifPluvialBuilding = CRSDiscountFactor
    ifPluvialContents = CRSDiscountFactor
    ssBuilding = CRSDiscountFactor
    ssContents = CRSDiscountFactor
    tsuBuilding = CRSDiscountFactor
    tsuContents = CRSDiscountFactor
    glBuilding = CRSDiscountFactor
    glContents = CRSDiscountFactor
    ceBuilding = CRSDiscountFactor
    ceContents = CRSDiscountFactor
    allPerils = CRSDiscountFactor

    CRSDiscountFactorResults_dict = {"items": item25,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("CRSDiscountFactorResults_dict  : ", CRSDiscountFactorResults_dict)
    CRSDiscountFactorResults = riskrating2resultsLevee(items=item25,
                                                       inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                       inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                       stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                       tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                       greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                       coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                       allPerilsAllCoverage=allPerils)
    CRSDiscountFactorResults.save()

    # Geographic Rate by Peril & Coverage
    componentList = ['ifFluvialBuilding', 'ifFluvialContents', 'ifPluvialBuilding', 'ifPluvialContents', 'ssBuilding', 'ssContents', 'tsuBuilding',
                     'tsuContents', 'glBuilding', 'glContents', 'ceBuilding', 'ceContents', 'allPerils']

    geographicRatebyPerilCoverage = []
    for x in componentList:
        geoRatingFuncList = [baserateResults_dict[x], distToRiverResults_dict[x], elevRelToRiverResults_dict[x], drainageAreaResults_dict[x], strucRelElvResults_dict[x],
                             distToCoastResults_dict[x], distToOceanResults_dict[x], elevationResults_dict[
                                 x], disttolakeResults_dict[x], elevationRelToLakeResults_dict[x], leveeQualityResults_dict[x],
                             territoryResults_dict[x]]
        y = 1
        for i in range(len(geoRatingFuncList)):
            if geoRatingFuncList[i] not in ['', -9999.0]:
                y *= geoRatingFuncList[i]
        geographicRatebyPerilCoverage.append(round(y, 4))

    item26 = "Geographic Rate by Peril & Coverage"
    ifFluvialBuilding = geographicRatebyPerilCoverage[0]
    ifFluvialContents = geographicRatebyPerilCoverage[1]
    ifPluvialBuilding = geographicRatebyPerilCoverage[2]
    ifPluvialContents = geographicRatebyPerilCoverage[3]
    ssBuilding = geographicRatebyPerilCoverage[4]
    ssContents = geographicRatebyPerilCoverage[5]
    tsuBuilding = geographicRatebyPerilCoverage[6]
    tsuContents = geographicRatebyPerilCoverage[7]
    glBuilding = geographicRatebyPerilCoverage[8]
    glContents = geographicRatebyPerilCoverage[9]
    ceBuilding = geographicRatebyPerilCoverage[10]
    ceContents = geographicRatebyPerilCoverage[11]
    allPerils = ''

    geographicRateResults_dict = {"items": item26,
                                  "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                  "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                  "glBuilding": glBuilding, "glContents": glContents,
                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                  "allPerils": allPerils}

    # print("geographicRateResults_dict  : ", geographicRateResults_dict)
    geographicRateResults = riskrating2resultsLevee(items=item26,
                                                    inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                    inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                    stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                    tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                    greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                    coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                    )
    geographicRateResults.save()

    # Rate by Peril & Coverage
    ratebyPerilCoverage = []
    for x in componentList:
        RatingFuncList = [geographicRateResults_dict[x], typeOfUseResults_dict[x], floorsOfIntResults_dict[x], foundationResults_dict[x], firstFloorHeightResults_dict[x],
                          meAbovefirstFloorResults_dict[x], coverageValueFactorResults_dict[x],  deductibleLimittoCoverageValueResults_dict[x]]
        y = 1
        for i in range(len(RatingFuncList)):
            if RatingFuncList[i] not in ['', -9999.0]:
                y *= RatingFuncList[i]
        ratebyPerilCoverage.append(round(y, 4))
    # print("RatebyPerilCoverage = ", ratebyPerilCoverage)

    # print("firstFloorHeightResults_dict = ",
    #       firstFloorHeightResults_dict.values())
    # print("coverageValueFactorResults_dict = ",
    #       coverageValueFactorResults_dict.values())
    # print("ratebyPerilCoverage = ", ratebyPerilCoverage)

    ratebyPerilCoverage1 = []
    for i, x in enumerate(componentList):
        if not (x == 'allPerils'):
            a = float(finalDeductibleITVResults_dict[x])
            b = float(CRSDiscountFactorResults_dict[x])
            c = float(ratebyPerilCoverage[i])

            y = a * b * c
            ratebyPerilCoverage1.append(round(y, 4))
    # print("RatebyPerilCoverage1 = ", ratebyPerilCoverage1)

    ratebyPerilCoverage1[0] = float(
        ratebyPerilCoverage1[0])*float(concRiskResults_dict['ifFluvialBuilding'])
    ratebyPerilCoverage1[1] = float(
        ratebyPerilCoverage1[1])*float(concRiskResults_dict['ifPluvialBuilding'])
    ratebyPerilCoverage1[2] = float(
        ratebyPerilCoverage1[2])*float(concRiskResults_dict['ifFluvialContents'])
    ratebyPerilCoverage1[3] = float(
        ratebyPerilCoverage1[3])*float(concRiskResults_dict['ifPluvialContents'])

    ratebyPerilCoverage1[4] = float(
        ratebyPerilCoverage1[4])*float(concRiskResults_dict['ssBuilding'])
    ratebyPerilCoverage1[5] = float(
        ratebyPerilCoverage1[5])*float(concRiskResults_dict['ssContents'])
    # print("RatebyPerilCoverage1 = ", ratebyPerilCoverage1)

    item27 = "Rate by Peril & Coverage"
    segment = ''

    ifFluvialBuilding = ratebyPerilCoverage1[0]
    ifFluvialContents = ratebyPerilCoverage1[1]
    ifPluvialBuilding = ratebyPerilCoverage1[2]
    ifPluvialContents = ratebyPerilCoverage1[3]
    ssBuilding = ratebyPerilCoverage1[4]
    ssContents = ratebyPerilCoverage1[5]
    tsuBuilding = ratebyPerilCoverage1[6]
    tsuContents = ratebyPerilCoverage1[7]
    glBuilding = ratebyPerilCoverage1[8]
    glContents = ratebyPerilCoverage1[9]
    ceBuilding = ratebyPerilCoverage1[10]
    ceContents = ratebyPerilCoverage1[11]
    allPerils = ''

    ratebyPerilCoverageResults_dict = {"items": item27, "Segment": segment,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("ratebyPerilCoverageResults_dict  : ", ratebyPerilCoverageResults_dict)
    ratebyPerilCoverageResults = riskrating2resultsLevee(items=item27,
                                                         inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                         inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
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
                              ratebyPerilCoverage1[8] +
                              ratebyPerilCoverage1[10]), 4)

    item28 = "Rate (per $1000 of Building Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = Rate_of_building

    rateBuildingValueResults_dict = {"items": item28,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("rateBuildingValueResults_dict  : ", rateBuildingValueResults_dict)
    rateBuildingValueResults = riskrating2resultsLevee(items=item28,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    rateBuildingValueResults.save()

    Rate_of_contents = round((ratebyPerilCoverage1[1] +
                              ratebyPerilCoverage1[3] +
                              ratebyPerilCoverage1[5] +
                              ratebyPerilCoverage1[7] +
                              ratebyPerilCoverage1[9] +
                              ratebyPerilCoverage1[11]), 4)

    item29 = "Rate (per $1000 of Contents Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = Rate_of_contents

    rateContentsValueResults_dict = {"items": item29,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("rateContentsValueResults_dict  : ", rateContentsValueResults_dict)
    rateContentsValueResults = riskrating2resultsLevee(items=item29,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    rateContentsValueResults.save()

    ifBuildingF_WbyC = round(
        (ratebyPerilCoverage1[0] / Rate_of_building)*100, 4)
    ifContentsF_WbyC = round(
        (ratebyPerilCoverage1[1] / Rate_of_contents)*100, 4)
    ifBuildingP_WbyC = round(
        (ratebyPerilCoverage1[2] / Rate_of_building)*100, 4)
    ifContentsP_WbyC = round(
        (ratebyPerilCoverage1[3] / Rate_of_contents)*100, 4)
    ssBuilding_WbyC = round(
        (ratebyPerilCoverage1[4] / Rate_of_building)*100, 4)
    ssContents_WbyC = round(
        (ratebyPerilCoverage1[5] / Rate_of_contents)*100, 4)
    tsuBuilding_WbyC = round(
        (ratebyPerilCoverage1[6] / Rate_of_building)*100, 4)
    tsuContents_WbyC = round(
        (ratebyPerilCoverage1[7] / Rate_of_contents)*100, 4)
    glBuilding_WbyC = round(
        (ratebyPerilCoverage1[8] / Rate_of_building)*100, 4)
    glContents_WbyC = round(
        (ratebyPerilCoverage1[9] / Rate_of_contents)*100, 4)
    ceBuilding_WbyC = round(
        (ratebyPerilCoverage1[10] / Rate_of_building)*100, 4)
    ceContents_WbyC = round(
        (ratebyPerilCoverage1[11] / Rate_of_contents)*100, 4)

    item30 = "Rate Weights by Coverage"
    ifFluvialBuilding = ifBuildingF_WbyC
    ifFluvialContents = ifContentsF_WbyC
    ifPluvialBuilding = ifBuildingP_WbyC
    ifPluvialContents = ifContentsP_WbyC
    ssBuilding = ssBuilding_WbyC
    ssContents = ssContents_WbyC
    tsuBuilding = tsuBuilding_WbyC
    tsuContents = tsuContents_WbyC
    glBuilding = glBuilding_WbyC
    glContents = glContents_WbyC
    ceBuilding = ceBuilding_WbyC
    ceContents = ceContents_WbyC
    allPerils = ''

    rateWeightsbyCoverageResults_dict = {"items": item30,
                                         "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                         "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                         "glBuilding": glBuilding, "glContents": glContents,
                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                         "allPerils": allPerils}

    # print("rateWeightsbyCoverageResults_dict  : ", rateWeightsbyCoverageResults_dict)
    rateWeightsbyCoverageResults = riskrating2resultsLevee(items=item30,
                                                           inlandFloodFluvialBuldings=ifFluvialBuilding, inlandFloodFluvialContents=ifFluvialContents,
                                                           inlandFloodPluvialBuldings=ifPluvialBuilding, inlandFloodPluvialContents=ifPluvialContents,
                                                           stormSurgeBuldings=ssBuilding, stormSurgeContents=ssContents,
                                                           tsunamiBuldings=tsuBuilding, tsunamiContents=tsuContents,
                                                           greatLakesBuldings=glBuilding, greatLakesContents=glContents,
                                                           coastalErosonBuldings=ceBuilding, coastalErosonContents=ceContents,
                                                           )
    rateWeightsbyCoverageResults.save()

    # Weighted Deductible & ITV Factor (Building)
    weighted_deductible_building = round((float(finalDeductibleITVResults_dict['ifFluvialBuilding']) * ifBuildingF_WbyC +
                                          float(finalDeductibleITVResults_dict['ifPluvialBuilding']) * ifBuildingP_WbyC +
                                          float(finalDeductibleITVResults_dict['ssBuilding']) * ssBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['tsuBuilding']) * tsuBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['glBuilding']) * glBuilding_WbyC +
                                          float(finalDeductibleITVResults_dict['ceBuilding']) * ceBuilding_WbyC)/100, 4)

    item31 = "Weighted Deductible & ITV Factor (Building)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = weighted_deductible_building

    weightedDeductibleITVBuildingResults_dict = {"items": item31,
                                                 "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                 "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                 "glBuilding": glBuilding, "glContents": glContents,
                                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                 "allPerils": allPerils}

    # print("weightedDeductibleITVBuildingResults_dict  : ", weightedDeductibleITVBuildingResults_dict)
    weightedDeductibleITVBuildingResults = riskrating2resultsLevee(items=item31,
                                                                   allPerilsAllCoverage=allPerils
                                                                   )
    weightedDeductibleITVBuildingResults.save()

    weighted_deductible_contents = round((float(finalDeductibleITVResults_dict['ifFluvialContents']) * ifContentsF_WbyC +
                                          float(finalDeductibleITVResults_dict['ifPluvialContents']) * ifContentsP_WbyC +
                                          float(finalDeductibleITVResults_dict['ssContents']) * ssContents_WbyC +
                                          float(finalDeductibleITVResults_dict['tsuContents']) * tsuContents_WbyC +
                                          float(finalDeductibleITVResults_dict['glContents']) * glContents_WbyC +
                                          float(finalDeductibleITVResults_dict['ceContents']) * ceContents_WbyC)/100, 4)

    item32 = "Weighted Deductible & ITV Factor (Contents)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = weighted_deductible_contents

    weightedDeductibleITVContentsResults_dict = {"items": item32,
                                                 "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                 "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                 "glBuilding": glBuilding, "glContents": glContents,
                                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                 "allPerils": allPerils}

    # print("weightedDeductibleITVContentsResults_dict  : ", weightedDeductibleITVContentsResults_dict)
    weightedDeductibleITVContentsResults = riskrating2resultsLevee(items=item32,
                                                                   allPerilsAllCoverage=allPerils
                                                                   )
    weightedDeductibleITVContentsResults.save()

    # Min and max rate- buildings
    min_rate_building = round(0 * weighted_deductible_building, 4)
    max_rate_building = round(15 * weighted_deductible_building, 4)

    item33 = "Minimum Rate (per $1000 of Building Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = min_rate_building

    min_rate_buildingResults_dict = {"items": item33,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("min_rate_buildingResults_dict  : ", min_rate_buildingResults_dict)
    min_rate_buildingResults = riskrating2resultsLevee(items=item33,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    min_rate_buildingResults.save()

    item34 = "Maximum Rate (per $1000 of Building Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = max_rate_building

    max_rate_buildingResults_dict = {"items": item34,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("max_rate_buildingResults_dict  : ", max_rate_buildingResults_dict)
    max_rate_buildingResults = riskrating2resultsLevee(items=item34,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    max_rate_buildingResults.save()

    # Min and max rate- contents
    min_rate_contents = round(0 * weighted_deductible_contents, 4)
    max_rate_contents = round(15 * weighted_deductible_contents, 4)

    item35 = "Minimum Rate (per $1000 of Contents Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = min_rate_contents

    min_rate_contentsResults_dict = {"items": item35,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("min_rate_contentsResults_dict  : ", min_rate_contentsResults_dict)
    min_rate_contentsResults = riskrating2resultsLevee(items=item35,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    min_rate_contentsResults.save()

    item36 = "Maximum Rate (per $1000 of Contents Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = max_rate_contents

    max_rate_contentsResults_dict = {"items": item36,
                                     "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                     "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                     "ssBuilding": ssBuilding, "ssContents": ssContents,
                                     "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                     "glBuilding": glBuilding, "glContents": glContents,
                                     "ceBuilding": ceBuilding, "ceContents": ceContents,
                                     "allPerils": allPerils}

    # print("max_rate_contentsResults_dict  : ", max_rate_contentsResults_dict)
    max_rate_contentsResults = riskrating2resultsLevee(items=item36,
                                                       allPerilsAllCoverage=allPerils
                                                       )
    max_rate_contentsResults.save()

    # min and max Rate by Peril & Coverage
    item37 = "Minimum Rate by Peril & Coverage (per $1000 of Coverage Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    min_rate_PerilCoverageResults_dict = {"items": item37,
                                          "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                          "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                          "ssBuilding": ssBuilding, "ssContents": ssContents,
                                          "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                          "glBuilding": glBuilding, "glContents": glContents,
                                          "ceBuilding": ceBuilding, "ceContents": ceContents,
                                          "allPerils": allPerils}

    # print("min_rate_PerilCoverageResults_dict  : ", min_rate_PerilCoverageResults_dict)
    min_rate_PerilCoverageResults = riskrating2resultsLevee(items=item37,
                                                            )
    min_rate_PerilCoverageResults.save()


#   Maximum Rate by Peril & Coverage (per $1000 of Coverage Value)
    item38 = "Maximum Rate by Peril & Coverage (per $1000 of Coverage Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = ''

    max_rate_PerilCoverageResults_dict = {"items": item38,
                                          "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                          "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                          "ssBuilding": ssBuilding, "ssContents": ssContents,
                                          "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                          "glBuilding": glBuilding, "glContents": glContents,
                                          "ceBuilding": ceBuilding, "ceContents": ceContents,
                                          "allPerils": allPerils}

    # print("max_rate_PerilCoverageResults_dict  : ", max_rate_PerilCoverageResults_dict)
    max_rate_PerilCoverageResults = riskrating2resultsLevee(items=item38
                                                            )
    max_rate_PerilCoverageResults.save()

    ############

    final_rate_building = min(
        max(Rate_of_building, min_rate_building), max_rate_building)
    final_rate_contents = min(
        max(Rate_of_contents, min_rate_contents), max_rate_contents)

#   Final Rate (per $1000 of Building Value)
    item39 = "Final Rate (per $1000 of Building Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = final_rate_building

    final_rate_buildingResults_dict = {"items": item39,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("final_rate_buildingResults_dict  : ", final_rate_buildingResults_dict)
    final_rate_buildingResults = riskrating2resultsLevee(items=item39,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    final_rate_buildingResults.save()

#   Final Rate (per $1000 of Contents Value)
    item40 = "Final Rate (per $1000 of Contents Value)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = final_rate_contents

    final_rate_contentsResults_dict = {"items": item40,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("final_rate_contentsResults_dict  : ",
    #       final_rate_contentsResults_dict)
    final_rate_contentsResults = riskrating2resultsLevee(items=item40,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    final_rate_contentsResults.save()

    coverage_building_thousands = currentScenario.buildingValue/1000
    coverage_contents_thousands = currentScenario.contentsValue/1000
    initial_premium_without_fees_building = final_rate_building * \
        coverage_building_thousands
    initial_premium_without_fees_contents = final_rate_contents * \
        coverage_contents_thousands
    initial_premium_without_fees = initial_premium_without_fees_building + \
        initial_premium_without_fees_contents

    priorClaim = str(currentScenario.priorClaimsID)
    prior_claim_premium = (float(priorClaim) * coverage_building_thousands *
                           weighted_deductible_building * max(0, float(priorClaim)-1))
    premium_exc_fees_expense = initial_premium_without_fees + prior_claim_premium
    premium_without_fees = premium_exc_fees_expense + \
        inputs['Loss Constant'] + inputs['Expense Constant']
    icc_crs = inputs['ICC premium'] * (100-currentScenario.crsRating.Value)/100
    subtotal = (premium_without_fees + icc_crs)

#   coverage_building_thousands

    item41 = "Coverage Value in Thousands (Buildings)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = coverage_building_thousands

    coverage_building_thousandsfinal_rate_contentsResults_dict = {"items": item41,
                                                                  "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                                  "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                                  "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                                  "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                                  "glBuilding": glBuilding, "glContents": glContents,
                                                                  "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                                  "allPerils": allPerils}

    # print("coverage_building_thousandsResults_dict  : ", coverage_building_thousandsResults_dict)
    coverage_building_thousandsResults = riskrating2resultsLevee(items=item41,
                                                                 allPerilsAllCoverage=allPerils
                                                                 )
    coverage_building_thousandsResults.save()

    # coverage_contents_thousands
    item42 = "Coverage Value in Thousands (Contents)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = coverage_contents_thousands

    coverage_contents_thousandsResults_dict = {"items": item42,
                                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                               "glBuilding": glBuilding, "glContents": glContents,
                                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                                               "allPerils": allPerils}

    # print("coverage_contents_thousandsResults_dict  : ",
    #       coverage_contents_thousandsResults_dict)
    coverage_contents_thousandsResults = riskrating2resultsLevee(items=item42,
                                                                 allPerilsAllCoverage=allPerils
                                                                 )
    coverage_contents_thousandsResults.save()

    # initial_premium_without_fees_building
    item43 = "Initial Premium without Fees (Buildings)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees_building
    initial_premium_without_fees_buildingResults_dict = {"items": item43,
                                                         "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                         "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                         "glBuilding": glBuilding, "glContents": glContents,
                                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                         "allPerils": allPerils}

    # print("initial_premium_without_fees_buildingResults_dict  : ",
    #       initial_premium_without_fees_buildingResults_dict)
    initial_premium_without_fees_buildingResults = riskrating2resultsLevee(items=item43,
                                                                           allPerilsAllCoverage=allPerils
                                                                           )
    initial_premium_without_fees_buildingResults.save()

#   initial_premium_without_fees_contents
    item44 = "Initial Premium without Fees (Contents)"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees_contents

    initial_premium_without_fees_contentsResults_dict = {"items": item44,
                                                         "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                         "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                         "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                         "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                         "glBuilding": glBuilding, "glContents": glContents,
                                                         "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                         "allPerils": allPerils}

    # print("initial_premium_without_fees_contentsResults_dict  : ",
    #       initial_premium_without_fees_contentsResults_dict)
    initial_premium_without_fees_contentsResults = riskrating2resultsLevee(items=item44,
                                                                           allPerilsAllCoverage=allPerils
                                                                           )
    initial_premium_without_fees_contentsResults.save()

    # initial_premium_without_fees
    item45 = "Initial Premium without Fees"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = initial_premium_without_fees

    initial_premium_without_feesResults_dict = {"items": item45,
                                                "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                                "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                                "ssBuilding": ssBuilding, "ssContents": ssContents,
                                                "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                                "glBuilding": glBuilding, "glContents": glContents,
                                                "ceBuilding": ceBuilding, "ceContents": ceContents,
                                                "allPerils": allPerils}

    # print("initial_premium_without_feesResults_dict  : ",
    #       initial_premium_without_feesResults_dict)
    initial_premium_without_feesResults = riskrating2resultsLevee(items=item45,
                                                                  allPerilsAllCoverage=allPerils
                                                                  )
    initial_premium_without_feesResults.save()


#   prior_claim_premium
    item46 = "Prior Claims Premium"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = prior_claim_premium

    prior_claim_premiumResults_dict = {"items": item46,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("prior_claim_premiumResults_dict  : ",
    #       prior_claim_premiumResults_dict)
    prior_claim_premiumResults = riskrating2resultsLevee(items=item46,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    prior_claim_premiumResults.save()

    # premium_exc_fees_expense
    item47 = "Premium excluding Fees & Expense Constant"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium_exc_fees_expense

    premium_exc_fees_expenseResults_dict = {"items": item47,
                                            "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                            "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                            "glBuilding": glBuilding, "glContents": glContents,
                                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                                            "allPerils": allPerils}

    # print("premium_exc_fees_expenseResults_dict  : ",
    #       premium_exc_fees_expenseResults_dict)
    premium_exc_fees_expenseResults = riskrating2resultsLevee(items=item47,
                                                              allPerilsAllCoverage=allPerils
                                                              )
    premium_exc_fees_expenseResults.save()

#   Expense Constant
    item48 = "Expense Constant"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Expense Constant']

    expense_ConstantResults_dict = {"items": item48,
                                    "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                    "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                    "ssBuilding": ssBuilding, "ssContents": ssContents,
                                    "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                    "glBuilding": glBuilding, "glContents": glContents,
                                    "ceBuilding": ceBuilding, "ceContents": ceContents,
                                    "allPerils": allPerils}

    # print("expense_ConstantResults_dict  : ", expense_ConstantResults_dict)
    expense_ConstantResults = riskrating2resultsLevee(items=item48,
                                                      allPerilsAllCoverage=allPerils
                                                      )
    expense_ConstantResults.save()

#   Loss Constant
    item49 = "Loss Constant"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Loss Constant']

    loss_ConstantResults_dict = {"items": item49,
                                 "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                 "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                 "ssBuilding": ssBuilding, "ssContents": ssContents,
                                 "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                 "glBuilding": glBuilding, "glContents": glContents,
                                 "ceBuilding": ceBuilding, "ceContents": ceContents,
                                 "allPerils": allPerils}

    # print("loss_ConstantResults_dict  : ", loss_ConstantResults_dict)
    loss_ConstantResults = riskrating2resultsLevee(items=item49,
                                                   allPerilsAllCoverage=allPerils
                                                   )
    loss_ConstantResults.save()

    #  premium_without_fees
    item50 = "Premium without Fees"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium_without_fees

    premium_without_feesResults_dict = {"items": item50,
                                        "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                        "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                        "ssBuilding": ssBuilding, "ssContents": ssContents,
                                        "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                        "glBuilding": glBuilding, "glContents": glContents,
                                        "ceBuilding": ceBuilding, "ceContents": ceContents,
                                        "allPerils": allPerils}

    # print("premium_without_feesResults_dict  : ", premium_without_feesResults_dict)
    premium_without_feesResults = riskrating2resultsLevee(items=item50,
                                                          allPerilsAllCoverage=allPerils
                                                          )
    premium_without_feesResults.save()


#   ICC premium
    item51 = "ICC Premium"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['ICC premium']

    icc_premiumResults_dict = {"items": item51,
                               "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                               "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                               "ssBuilding": ssBuilding, "ssContents": ssContents,
                               "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                               "glBuilding": glBuilding, "glContents": glContents,
                               "ceBuilding": ceBuilding, "ceContents": ceContents,
                               "allPerils": allPerils}

    # print("icc_premiumResults_dict  : ", icc_premiumResults_dict)
    icc_premiumResults = riskrating2resultsLevee(items=item51,
                                                 allPerilsAllCoverage=allPerils
                                                 )
    icc_premiumResults.save()

#   icc_crs
    item52 = "ICC Premium with CRS Discount"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = icc_crs

    icc_crsResults_dict = {"items": item52,
                           "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                           "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                           "ssBuilding": ssBuilding, "ssContents": ssContents,
                           "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                           "glBuilding": glBuilding, "glContents": glContents,
                           "ceBuilding": ceBuilding, "ceContents": ceContents,
                           "allPerils": allPerils}

    # print("icc_crsResults_dict  : ", icc_crsResults_dict)
    icc_crsResults = riskrating2resultsLevee(items=item52,
                                             allPerilsAllCoverage=allPerils
                                             )
    icc_crsResults.save()

    # subtotal
    item53 = "Subtotal"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = subtotal

    subtotalResults_dict = {"items": item53,
                            "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                            "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                            "ssBuilding": ssBuilding, "ssContents": ssContents,
                            "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                            "glBuilding": glBuilding, "glContents": glContents,
                            "ceBuilding": ceBuilding, "ceContents": ceContents,
                            "allPerils": allPerils}

    # print("subtotalResults_dict  : ", subtotalResults_dict)
    subtotalResults = riskrating2resultsLevee(items=item53,
                                              allPerilsAllCoverage=allPerils
                                              )
    subtotalResults.save()

#   Reserve fund
    item54 = "Reserve Fund Factor"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Reserve fund']

    reserve_fund_factorResults_dict = {"items": item54,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("reserve_fund_factorResults_dict  : ", reserve_fund_factorResults_dict)
    reserve_fund_factorResults = riskrating2resultsLevee(items=item54,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    reserve_fund_factorResults.save()

    # subtotal = subtotal * inputs['Reserve fund']
    # subtotal
    subtotal_with_reservefund = subtotal * inputs['Reserve fund']

    item55 = "Subtotal with Reserve Fund"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = subtotal_with_reservefund

    subtotal_with_reservefundResults_dict = {"items": item55,
                                             "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                             "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                             "ssBuilding": ssBuilding, "ssContents": ssContents,
                                             "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                             "glBuilding": glBuilding, "glContents": glContents,
                                             "ceBuilding": ceBuilding, "ceContents": ceContents,
                                             "allPerils": allPerils}

    # print("subtotal_with_reservefundResults_dict  : ",
    #        subtotal_with_reservefundResults_dict)
    subtotal_with_reservefundResults = riskrating2resultsLevee(items=item55,
                                                               allPerilsAllCoverage=allPerils
                                                               )
    subtotal_with_reservefundResults.save()

    # Probation surcharge
    item56 = "Probation Surcharge"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Probation surcharge']

    probation_surchargeResults_dict = {"items": item56,
                                       "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                       "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                       "ssBuilding": ssBuilding, "ssContents": ssContents,
                                       "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                       "glBuilding": glBuilding, "glContents": glContents,
                                       "ceBuilding": ceBuilding, "ceContents": ceContents,
                                       "allPerils": allPerils}

    # print("probation_surchargeResults_dict  : ", probation_surchargeResults_dict)
    probation_surchargeResults = riskrating2resultsLevee(items=item56,
                                                         allPerilsAllCoverage=allPerils
                                                         )
    probation_surchargeResults.save()

    if str(currentScenario.primaryResidenceIndicatorID) == 'Yes':
        HFIAA_surcharge = 50
    else:
        HFIAA_surcharge = 250
#   HFIAA_surcharge
    item57 = "HFIAA Surcharge by Primary Residence Indicator"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = HFIAA_surcharge

    hfiaa_surchargeResults_dict = {"items": item57,
                                   "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                   "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                   "ssBuilding": ssBuilding, "ssContents": ssContents,
                                   "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                   "glBuilding": glBuilding, "glContents": glContents,
                                   "ceBuilding": ceBuilding, "ceContents": ceContents,
                                   "allPerils": allPerils}

    # print("hfiaa_surchargeResults_dict  : ", hfiaa_surchargeResults_dict)
    hfiaa_surchargeResults = riskrating2resultsLevee(items=item57,
                                                     allPerilsAllCoverage=allPerils
                                                     )
    hfiaa_surchargeResults.save()

#   Federal policy fee
    item58 = "Federal Policy Fee"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = inputs['Federal policy fee']

    federal_policy_feeResults_dict = {"items": item58,
                                      "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                                      "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                                      "ssBuilding": ssBuilding, "ssContents": ssContents,
                                      "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                                      "glBuilding": glBuilding, "glContents": glContents,
                                      "ceBuilding": ceBuilding, "ceContents": ceContents,
                                      "allPerils": allPerils}

    # print("federal_policy_feeResults_dict  : ", federal_policy_feeResults_dict)
    federal_policy_feeResults = riskrating2resultsLevee(items=item58,
                                                        allPerilsAllCoverage=allPerils
                                                        )
    federal_policy_feeResults.save()

    premium = round(subtotal_with_reservefund + inputs['Probation surcharge'] +
                    HFIAA_surcharge + inputs['Federal policy fee'], 2)

#   premium
    item59 = "Premium with Fees"
    ifFluvialBuilding = ''
    ifFluvialContents = ''
    ifPluvialBuilding = ''
    ifPluvialContents = ''
    ssBuilding = ''
    ssContents = ''
    tsuBuilding = ''
    tsuContents = ''
    glBuilding = ''
    glContents = ''
    ceBuilding = ''
    ceContents = ''
    allPerils = premium

    premiumResults_dict = {"items": item59,
                           "ifFluvialBuilding": ifFluvialBuilding, "ifFluvialContents": ifFluvialContents,
                           "ifPluvialBuilding": ifPluvialBuilding, "ifPluvialContents": ifPluvialContents,
                           "ssBuilding": ssBuilding, "ssContents": ssContents,
                           "tsuBuilding": tsuBuilding, "tsuContents": tsuContents,
                           "glBuilding": glBuilding, "glContents": glContents,
                           "ceBuilding": ceBuilding, "ceContents": ceContents,
                           "allPerils": allPerils}

    # print("premiumResults_dict  : ", premiumResults_dict)
    premiumResults = riskrating2resultsLevee(items=item59,
                                             allPerilsAllCoverage=allPerils
                                             )
    premiumResults.save()

    return [{"baserate results": baserateResults_dict["allPerils"]}, {"distToRiver results": distToRiverResults_dict["allPerils"]},
            {"elevRelToRiver Results":
                elevRelToRiverResults_dict["allPerils"]},
            {"drainageArea Results": drainageAreaResults_dict["allPerils"]}, {
                "strucRelElv Results": strucRelElvResults_dict["allPerils"]},
            {"distToCoast Results": distToCoastResults_dict["allPerils"]},
            {"distToOcean Results": distToOceanResults_dict["allPerils"]}, {
                "elevation Results": elevationResults_dict["allPerils"]},
            {"disttolake Results": disttolakeResults_dict["allPerils"]}, {
                "elevationRelToLake Results": elevationRelToLakeResults_dict["allPerils"]},
            {"leveeQuality Results": leveeQualityResults_dict["allPerils"]}, {
                "territory Results": territoryResults_dict["allPerils"]},
            {"typeOfUse Results": typeOfUseResults_dict["allPerils"]}, {
                "floorsOfInt Results": floorsOfIntResults_dict["allPerils"]},
            {"foundation Results": foundationResults_dict["allPerils"]}, {
                "firstFloorHeight Results": firstFloorHeightResults_dict["allPerils"]},
            {"meAbovefirstFloor Results": meAbovefirstFloorResults_dict["allPerils"]}, {
                "coverageValueFactor Results": coverageValueFactorResults_dict["allPerils"]},
            {"deductibleLimittoCoverageValue Results":
                deductibleLimittoCoverageValueResults_dict["allPerils"]},
            {"deductibletoCoverageValue Results":
                deductibletoCoverageValueResults_dict["allPerils"]},
            {"initialDeductibleITV Results":
                initialDeductibleITVResults_dict["allPerils"]},
            {"finalDeductibleITV Results":
                finalDeductibleITVResults_dict["allPerils"]},
            {"concRisk Results": concRiskResults_dict["allPerils"]}, {
                "CRSDiscountPerc Results": CRSDiscountPercResults_dict["allPerils"]},
            {"CRSDiscountFactor Results":
                CRSDiscountFactorResults_dict["allPerils"]},
            {"geographicRate Results":
                geographicRateResults_dict["allPerils"]},
            {"ratebyPerilCoverage Results":
                ratebyPerilCoverageResults_dict["allPerils"]},
            {"rateBuildingValue Results": rateBuildingValueResults_dict["allPerils"]}, {
                "rateContentsValue Results": rateContentsValueResults_dict["allPerils"]},
            {"rateWeightsbyCoverage Results":
                rateWeightsbyCoverageResults_dict["allPerils"]},
            {"weightedDeductibleITVBuilding Results":
                weightedDeductibleITVBuildingResults_dict["allPerils"]},
            {"weightedDeductibleITVContents Results":
                weightedDeductibleITVContentsResults_dict["allPerils"]},
            {"min_rate_building Results":
                min_rate_buildingResults_dict["allPerils"]},
            {"max_rate_building Results":
                max_rate_buildingResults_dict["allPerils"]},
            {"min_rate_contents Results":
                min_rate_contentsResults_dict["allPerils"]},
            {"max_rate_contents Results":
                max_rate_contentsResults_dict["allPerils"]},
            {"min_rate_PerilCoverage Results":
                min_rate_PerilCoverageResults_dict["allPerils"]},
            {"max_rate_PerilCoverage Results":
                max_rate_PerilCoverageResults_dict["allPerils"]},
            {"final_rate_building Results":
                final_rate_buildingResults_dict["allPerils"]},
            {"final_rate_contents Results":
                final_rate_contentsResults_dict["allPerils"]},
            {"coverage_building_thousandsfinal_rate_contents Results":
                coverage_building_thousandsfinal_rate_contentsResults_dict["allPerils"]},
            {"coverage_contents_thousands Results":
                coverage_contents_thousandsResults_dict["allPerils"]},
            {"initial_premium_without_fees_building Results":
                initial_premium_without_fees_buildingResults_dict["allPerils"]},
            {"initial_premium_without_fees_contents Results":
                initial_premium_without_fees_contentsResults_dict["allPerils"]},
            {"initial_premium_without_fees Results":
                initial_premium_without_feesResults_dict["allPerils"]},
            {"prior_claim_premium Results":
                prior_claim_premiumResults_dict["allPerils"]},
            {"premium_exc_fees_expense Results":
                premium_exc_fees_expenseResults_dict["allPerils"]},
            {"expense_Constant Results":
                expense_ConstantResults_dict["allPerils"]},
            {"loss_Constant Results": loss_ConstantResults_dict["allPerils"]},
            {"premium_without_fees Results":
                premium_without_feesResults_dict["allPerils"]},
            {"icc_premium Results": icc_premiumResults_dict["allPerils"]},
            {"icc_crs Results": icc_crsResults_dict["allPerils"]},
            {"subtotal Results": subtotalResults_dict["allPerils"]},
            {"reserve_fund_factor Results":
                reserve_fund_factorResults_dict["allPerils"]},
            {"subtotal_with_reservefund Results":
                subtotal_with_reservefundResults_dict["allPerils"]},
            {"probation_surcharge Results":
                probation_surchargeResults_dict["allPerils"]},
            {"hfiaa_surcharge Results":
                hfiaa_surchargeResults_dict["allPerils"]},
            {"federal_policy_fee Results":
                federal_policy_feeResults_dict["allPerils"]},
            {"premium Results": premiumResults_dict["allPerils"]}]
