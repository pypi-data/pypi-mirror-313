"""Test the LaMarzoccoMachine class."""

# pylint: disable=W0212

from dataclasses import asdict
from http import HTTPMethod

from aioresponses import aioresponses
from syrupy import SnapshotAssertion

from pylamarzocco.clients.bluetooth import LaMarzoccoBluetoothClient
from pylamarzocco.clients.cloud import LaMarzoccoCloudClient
from pylamarzocco.clients.local import LaMarzoccoLocalClient
from pylamarzocco.const import BoilerType, PhysicalKey

from . import init_machine
from .conftest import load_fixture


async def test_create(
    cloud_client: LaMarzoccoCloudClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test creation of a cloud client."""

    machine = await init_machine(cloud_client)
    assert asdict(machine.config) == snapshot(name="config")
    assert machine.firmware == snapshot(name="firmware")
    assert machine.statistics == snapshot(name="statistics")


async def test_local_client(
    local_machine_client: LaMarzoccoLocalClient,
    cloud_client: LaMarzoccoCloudClient,
    mock_aioresponse: aioresponses,
) -> None:
    """Ensure that the local client delivers same result"""
    # load config
    mock_aioresponse.get(
        url="http://192.168.1.42:8081/api/v1/config",
        status=200,
        payload=load_fixture("machine", "config.json")["data"],
    )

    machine = await init_machine(local_client=local_machine_client)

    machine2 = await init_machine(cloud_client)

    assert machine
    assert str(machine.config) == str(machine2.config)


async def test_set_temp(
    cloud_client: LaMarzoccoCloudClient,
) -> None:
    """Test setting boiler temperature."""
    machine = await init_machine(cloud_client)

    result = await machine.set_temp(
        BoilerType.STEAM,
        120,
    )
    assert result is True
    assert machine.config.boilers[BoilerType.STEAM].target_temperature == 120


# async def test_set_schedule(
#     cloud_client: LaMarzoccoCloudClient,
# ) -> None:
#     """Test setting prebrew infusion."""
#     machine = await init_machine(cloud_client)

#     with patch("asyncio.sleep", new_callable=AsyncMock):
#         result = await machine.set_schedule_day(
#             day=WeekDay.MONDAY,
#             enabled=True,
#             h_on=3,
#             m_on=0,
#             h_off=24,
#             m_off=0,
#         )
#     assert result is True


async def test_websocket_message(
    cloud_client: LaMarzoccoCloudClient,
    local_machine_client: LaMarzoccoLocalClient,
    snapshot: SnapshotAssertion,
):
    """Test parsing of websocket messages."""
    machine = await init_machine(cloud_client, local_client=local_machine_client)

    message = r'[{"Boilers":"[{\"id\":\"SteamBoiler\",\"isEnabled\":true,\"target\":131,\"current\":113},{\"id\":\"CoffeeBoiler1\",\"isEnabled\":true,\"target\":94,\"current\":81}]"}]'
    machine.on_websocket_message_received(message)
    assert asdict(machine.config) == snapshot

    message = r'[{"BoilersTargetTemperature":"{\"SteamBoiler\":131,\"CoffeeBoiler1\":94}"},{"Boilers":"[{\"id\":\"SteamBoiler\",\"isEnabled\":true,\"target\":131,\"current\":50},{\"id\":\"CoffeeBoiler1\",\"isEnabled\":true,\"target\":94,\"current\":36}]"}]'
    machine.on_websocket_message_received(message)
    assert asdict(machine.config) == snapshot


async def test_set_power(
    cloud_client: LaMarzoccoCloudClient,
    bluetooth_client: LaMarzoccoBluetoothClient,
    mock_aioresponse: aioresponses,
):
    """Test setting the power."""
    machine = await init_machine(cloud_client, bluetooth_client=bluetooth_client)

    assert await machine.set_power(True)

    bluetooth_client._client.write_gatt_char.assert_called_once_with(  # type: ignore[attr-defined]
        "050b7847-e12b-09a8-b04b-8e0922a9abab",
        b'{"name":"MachineChangeMode","parameter":{"mode":"BrewingMode"}}\x00',
    )
    mock_aioresponse.assert_any_call(  # type: ignore[attr-defined]
        method=HTTPMethod.POST,
        url="https://gw-lmz.lamarzocco.io/v1/home/machines/GS01234/status",
        json={"status": "BrewingMode"},
        timeout=5,
        headers={"Authorization": "Bearer token"},
    )


async def test_set_steam(
    cloud_client: LaMarzoccoCloudClient,
    bluetooth_client: LaMarzoccoBluetoothClient,
    mock_aioresponse: aioresponses,
):
    """Test setting the steam."""
    machine = await init_machine(cloud_client, bluetooth_client=bluetooth_client)

    assert await machine.set_steam(True)

    bluetooth_client._client.write_gatt_char.assert_called_once_with(  # type: ignore[attr-defined]
        "050b7847-e12b-09a8-b04b-8e0922a9abab",
        b'{"name":"SettingBoilerEnable","parameter":{"identifier":"SteamBoiler","state":true}}\x00',
    )
    mock_aioresponse.assert_any_call(  # type: ignore[attr-defined]
        method=HTTPMethod.POST,
        url="https://gw-lmz.lamarzocco.io/v1/home/machines/GS01234/enable-boiler",
        json={"identifier": "SteamBoiler", "state": True},
        timeout=5,
        headers={"Authorization": "Bearer token"},
    )


async def test_set_temperature(
    cloud_client: LaMarzoccoCloudClient,
    bluetooth_client: LaMarzoccoBluetoothClient,
    mock_aioresponse: aioresponses,
):
    """Test setting temperature."""
    machine = await init_machine(cloud_client, bluetooth_client=bluetooth_client)

    assert await machine.set_temp(BoilerType.STEAM, 131)

    bluetooth_client._client.write_gatt_char.assert_called_once_with(  # type: ignore[attr-defined]
        "050b7847-e12b-09a8-b04b-8e0922a9abab",
        b'{"name":"SettingBoilerTarget","parameter":{"identifier":"SteamBoiler","value":131}}\x00',
    )
    mock_aioresponse.assert_any_call(  # type: ignore[attr-defined]
        method=HTTPMethod.POST,
        url="https://gw-lmz.lamarzocco.io/v1/home/machines/GS01234/target-boiler",
        json={"identifier": "SteamBoiler", "value": 131},
        timeout=5,
        headers={"Authorization": "Bearer token"},
    )


async def test_set_prebrew_time(
    cloud_client: LaMarzoccoCloudClient,
    mock_aioresponse: aioresponses,
):
    """Test setting prebrew time."""
    machine = await init_machine(
        cloud_client,
    )

    assert await machine.set_prebrew_time(1.0, 3.5)

    mock_aioresponse.assert_any_call(  # type: ignore[attr-defined]
        method=HTTPMethod.POST,
        url="https://gw-lmz.lamarzocco.io/v1/home/machines/GS01234/setting-preinfusion",
        json={
            "button": "DoseA",
            "group": "Group1",
            "holdTimeMs": 3500,
            "wetTimeMs": 1000,
        },
        timeout=5,
        headers={"Authorization": "Bearer token"},
    )

    assert machine.config.prebrew_configuration[PhysicalKey.A].on_time == 1.0
    assert machine.config.prebrew_configuration[PhysicalKey.A].off_time == 3.5


async def test_set_preinfusion_time(
    cloud_client: LaMarzoccoCloudClient,
    mock_aioresponse: aioresponses,
):
    """Test setting prebrew time."""
    machine = await init_machine(
        cloud_client,
    )
    assert await machine.set_preinfusion_time(4.5)
    mock_aioresponse.assert_any_call(  # type: ignore[attr-defined]
        method=HTTPMethod.POST,
        url="https://gw-lmz.lamarzocco.io/v1/home/machines/GS01234/setting-preinfusion",
        json={"button": "DoseA", "group": "Group1", "holdTimeMs": 4500, "wetTimeMs": 0},
        timeout=5,
        headers={"Authorization": "Bearer token"},
    )

    assert machine.config.prebrew_configuration[PhysicalKey.A].off_time == 4.5
