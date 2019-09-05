#
#    Copyright (c) 2018-2019 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Test module weewx.wxformulas"""

import unittest

try:
    # Python 3 --- mock is included in unittest
    from unittest import mock
except ImportError:
    # Python 2 --- must have mock installed
    import mock

import weeutil.xtypes
import weewx.wxformulas


class WXFormulasTest(unittest.TestCase):

    def test_dewpoint(self):
        self.assertAlmostEqual(weewx.wxformulas.dewpointF(68, 50), 48.7, 1)
        self.assertAlmostEqual(weewx.wxformulas.dewpointF(32, 50), 15.5, 1)
        self.assertAlmostEqual(weewx.wxformulas.dewpointF(-10, 50), -23.5, 1)
        self.assertIsNone(weewx.wxformulas.dewpointF(-10, None))
        self.assertIsNone(weewx.wxformulas.dewpointF(-10, 0))

    def test_windchill(self):
        self.assertAlmostEqual(weewx.wxformulas.windchillF(55, 20), 55.0, 0)
        self.assertAlmostEqual(weewx.wxformulas.windchillF(45, 2), 45.0, 0)
        self.assertAlmostEqual(weewx.wxformulas.windchillF(45, 20), 37.0, 0)
        self.assertAlmostEqual(weewx.wxformulas.windchillF(-5, 20), -29.0, 0)
        self.assertIsNone(weewx.wxformulas.windchillF(55, None))

        self.assertAlmostEqual(weewx.wxformulas.windchillC(12, 30), 12, 0)
        self.assertAlmostEqual(weewx.wxformulas.windchillC(5, 30), 0, 0)
        self.assertAlmostEqual(weewx.wxformulas.windchillC(5, 3), 5, 0)
        self.assertIsNone(weewx.wxformulas.windchillC(5, None))

    def test_heatindex(self):
        self.assertAlmostEqual(weewx.wxformulas.heatindexF(75.0, 50.0), 75.0, 1)
        self.assertAlmostEqual(weewx.wxformulas.heatindexF(80.0, 50.0), 80.8, 1)
        self.assertAlmostEqual(weewx.wxformulas.heatindexF(80.0, 95.0), 86.4, 1)
        self.assertAlmostEqual(weewx.wxformulas.heatindexF(90.0, 50.0), 94.6, 1)
        self.assertAlmostEqual(weewx.wxformulas.heatindexF(90.0, 95.0), 126.6, 1)
        self.assertIsNone(weewx.wxformulas.heatindexF(90, None))

        self.assertAlmostEqual(weewx.wxformulas.heatindexC(30, 80), 37.7, 1)
        self.assertIsNone(weewx.wxformulas.heatindexC(30, None))

    def test_altimeter_pressure(self):
        self.assertAlmostEqual(weewx.wxformulas.altimeter_pressure_US(28.0, 0.0), 28.002, 3)
        self.assertAlmostEqual(weewx.wxformulas.altimeter_pressure_US(28.0, 1000.0), 29.043, 3)
        self.assertIsNone(weewx.wxformulas.altimeter_pressure_US(28.0, None))
        self.assertAlmostEqual(weewx.wxformulas.altimeter_pressure_Metric(948.08, 0.0), 948.2, 1)
        self.assertAlmostEqual(weewx.wxformulas.altimeter_pressure_Metric(948.08, 304.8), 983.4, 1)
        self.assertIsNone(weewx.wxformulas.altimeter_pressure_Metric(948.08, None))

    def test_solar_rad(self):
        results = [weewx.wxformulas.solar_rad_Bras(42, -72, 0, t * 3600 + 1422936471) for t in range(24)]
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 1.86, 100.81, 248.71,
                    374.68, 454.90, 478.76, 443.47, 353.23, 220.51, 73.71, 0, 0, 0,
                    0, 0, 0]
        for result, expect in zip(results, expected):
            self.assertAlmostEqual(result, expect, 2)

        results = [weewx.wxformulas.solar_rad_RS(42, -72, 0, t * 3600 + 1422936471) for t in range(24)]
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0.09, 79.31, 234.77,
                    369.80, 455.66, 481.15, 443.44, 346.81, 204.64, 52.63, 0, 0, 0,
                    0, 0, 0]
        for result, expect in zip(results, expected):
            self.assertAlmostEqual(result, expect, 2)

    def test_humidex(self):
        self.assertAlmostEqual(weewx.wxformulas.humidexC(30.0, 80.0), 43.64, 2)
        self.assertAlmostEqual(weewx.wxformulas.humidexC(30.0, 20.0), 30.00, 2)
        self.assertAlmostEqual(weewx.wxformulas.humidexC(0.0, 80.0), 0, 2)
        self.assertIsNone(weewx.wxformulas.humidexC(30.0, None))

    def test_equation_of_time(self):
        # 1 October
        self.assertAlmostEqual(weewx.wxformulas.equation_of_time(274), 0.1889, 4)

    def test_hour_angle(self):
        self.assertAlmostEqual(weewx.wxformulas.hour_angle(15.5, -16.25, 274), 0.6821, 4)
        self.assertAlmostEqual(weewx.wxformulas.hour_angle(0, -16.25, 274), 2.9074, 4)

    def test_solar_declination(self):
        # 1 October
        self.assertAlmostEqual(weewx.wxformulas.solar_declination(274), -0.075274, 6)

    def test_sun_radiation(self):
        self.assertAlmostEqual(weewx.wxformulas.sun_radiation(doy=274,
                                                              latitude_deg=16.217, longitude_deg=-16.25,
                                                              tod_utc=16.0,
                                                              interval=1.0), 3.543, 3)

    def test_longwave_radiation(self):
        # In mm/day
        self.assertAlmostEqual(weewx.wxformulas.longwave_radiation(Tmin_C=19.1, Tmax_C=25.1,
                                                                   ea=2.1, Rs=14.5, Rso=18.8, rh=50), 3.5, 1)
        self.assertAlmostEqual(weewx.wxformulas.longwave_radiation(Tmin_C=28, Tmax_C=28,
                                                                   ea=3.402, Rs=0, Rso=0, rh=40), 2.4, 1)

    def test_ET(self):
        sr_mean_wpm2 = 680.56  # == 2.45 MJ/m^2/hr
        timestamp = 1475337600  # 1-Oct-2016 at 16:00UTC
        self.assertAlmostEqual(weewx.wxformulas.evapotranspiration_Metric(Tmin_C=38, Tmax_C=38,
                                                                          rh_min=52, rh_max=52,
                                                                          sr_mean_wpm2=sr_mean_wpm2,
                                                                          ws_mps=3.3,
                                                                          wind_height_m=2,
                                                                          latitude_deg=16.217,
                                                                          longitude_deg=-16.25,
                                                                          altitude_m=8, timestamp=timestamp), 0.63, 2)

        sr_mean_wpm2 = 0.0  # Night time
        timestamp = 1475294400  # 1-Oct-2016 at 04:00UTC (0300 local)
        self.assertAlmostEqual(weewx.wxformulas.evapotranspiration_Metric(Tmin_C=28, Tmax_C=28,
                                                                          rh_min=90, rh_max=90,
                                                                          sr_mean_wpm2=sr_mean_wpm2,
                                                                          ws_mps=3.3,
                                                                          wind_height_m=2,
                                                                          latitude_deg=16.217,
                                                                          longitude_deg=-16.25,
                                                                          altitude_m=8, timestamp=timestamp), 0.03, 2)
        sr_mean_wpm2 = 860
        timestamp = 1469829600  # 29-July-2016 22:00 UTC (15:00 local time)
        self.assertAlmostEqual(weewx.wxformulas.evapotranspiration_US(Tmin_F=87.8, Tmax_F=89.1,
                                                                      rh_min=34, rh_max=38,
                                                                      sr_mean_wpm2=sr_mean_wpm2, ws_mph=9.58,
                                                                      wind_height_ft=6,
                                                                      latitude_deg=45.7, longitude_deg=-121.5,
                                                                      altitude_ft=700, timestamp=timestamp), 0.028, 3)


# Test values for the PressureCooker test:
record = {
    'dateTime': 1567515300, 'usUnits': 1, 'interval': 5, 'inTemp': 73.0, 'outTemp': 55.7, 'inHumidity': 54.0,
    'outHumidity': 90.0, 'windSpeed': 0.0, 'windDir': None, 'windGust': 2.0, 'windGustDir': 270.0,
    'rain': 0.0, 'windchill': 55.7, 'heatindex': 55.7
}
# These are the correct values
pressure = 29.259303850622302
barometer = 29.99
altimeter = 30.001561119603156


class TestPressureCooker(unittest.TestCase):
    """Test the class PressureCooker"""

    def setUp(self):
        # Make a copy. We will be modifying it.
        self.record = dict(record)

    def test_get_temperature_12h_F(self):
        db_manager = mock.Mock()
        pc = weewx.wxformulas.PressureCooker(700, db_manager)

        # Mock a database in US units
        with mock.patch.object(db_manager, 'getRecord',
                               return_value={'usUnits': weewx.US, 'outTemp': 80.3}) as mock_mgr:
            t = pc._get_temperature_12h_F(self.record['dateTime'])
            # Make sure the mocked database manager got called with a time 12h ago
            mock_mgr.assert_called_once_with(self.record['dateTime'] - 12 * 3600, max_delta=1800)
            self.assertEqual(t, 80.3)

        # Mock a database in METRICWX units
        with mock.patch.object(db_manager, 'getRecord',
                               return_value={'usUnits': weewx.METRICWX, 'outTemp': 30.0}) as mock_mgr:
            t = pc._get_temperature_12h_F(self.record['dateTime'])
            mock_mgr.assert_called_once_with(self.record['dateTime'] - 12 * 3600, max_delta=1800)
            self.assertEqual(t, 86)

    def test_calc_pressure(self):
        # To calculate station pressure, we need barometric pressure. Add it
        self.record['barometer'] = barometer
        # Mock up a database manager
        db_manager = mock.Mock()
        # Create a pressure cooker with our mocked manager
        pc = weewx.wxformulas.PressureCooker(700, db_manager)

        # Mock a result set in US units
        with mock.patch.object(db_manager, 'getRecord',
                               return_value={'usUnits': weewx.US, 'outTemp': 80.3}):
            p = pc.calc_pressure(self.record)
            self.assertEqual(p, pressure)

        # Try it using the "calc()" entry point:
        with mock.patch.object(db_manager, 'getRecord',
                               return_value={'usUnits': weewx.US, 'outTemp': 80.3}):
            self.assertEqual(pc.calc('pressure', self.record), pressure)

    def test_bound_method(self):
        """Do a test, this time using a bound method (instead of a simple function)"""
        # To calculate station pressure, we need barometric pressure. Add it
        self.record['barometer'] = barometer
        # Mock up a database manager
        db_manager = mock.Mock()
        # Create a pressure cooker with our mocked manager
        pc = weewx.wxformulas.PressureCooker(700, db_manager)
        # Use a bound method for the extension function
        xt = weeutil.xtypes.ExtendedTypes(self.record, {'pressure': pc.calc})

        # Mock a result set in US units
        with mock.patch.object(db_manager, 'getRecord',
                               return_value={'usUnits': weewx.US, 'outTemp': 80.3}):
            self.assertEqual(xt['pressure'], pressure)


unittest.main()
