// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.github.google.bumble.btbench

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.github.google.bumble.btbench.ui.theme.BTBenchTheme
import java.util.logging.Logger

private val Log = Logger.getLogger("bumble.main-activity")

const val PEER_BLUETOOTH_ADDRESS_PREF_KEY = "peer_bluetooth_address"
const val SENDER_PACKET_COUNT_PREF_KEY = "sender_packet_count"
const val SENDER_PACKET_SIZE_PREF_KEY = "sender_packet_size"
const val SENDER_PACKET_INTERVAL_PREF_KEY = "sender_packet_interval"
const val SCENARIO_PREF_KEY = "scenario"
const val MODE_PREF_KEY = "mode"

class MainActivity : ComponentActivity() {
    private val appViewModel = AppViewModel()
    private var bluetoothAdapter: BluetoothAdapter? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        appViewModel.loadPreferences(getPreferences(Context.MODE_PRIVATE))
        checkPermissions()
    }

    private fun checkPermissions() {
        val neededPermissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(
                Manifest.permission.BLUETOOTH_ADVERTISE,
                Manifest.permission.BLUETOOTH_SCAN,
                Manifest.permission.BLUETOOTH_CONNECT
            )
        } else {
            arrayOf(Manifest.permission.BLUETOOTH, Manifest.permission.BLUETOOTH_ADMIN)
        }
        val missingPermissions = neededPermissions.filter {
            ContextCompat.checkSelfPermission(baseContext, it) != PackageManager.PERMISSION_GRANTED
        }

        if (missingPermissions.isEmpty()) {
            start()
            return
        }

        val requestPermissionsLauncher = registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            permissions.entries.forEach {
                Log.info("permission: ${it.key} = ${it.value}")
            }
            val grantCount = permissions.count { it.value }
            if (grantCount == neededPermissions.size) {
                // We have all the permissions we need.
                start()
            } else {
                Log.warning("not all permissions granted")
            }
        }

        requestPermissionsLauncher.launch(missingPermissions.toTypedArray())
        return
    }

    @SuppressLint("MissingPermission")
    private fun initBluetooth() {
        val bluetoothManager = ContextCompat.getSystemService(this, BluetoothManager::class.java)
        bluetoothAdapter = bluetoothManager?.adapter

        if (bluetoothAdapter == null) {
            Log.warning("no bluetooth adapter")
            return
        }

        if (!bluetoothAdapter!!.isEnabled) {
            Log.warning("bluetooth not enabled")
            return
        }
    }

    private fun start() {
        initBluetooth()
        setContent {
            MainView(
                appViewModel,
                ::becomeDiscoverable,
                ::runScenario
            )
        }

        // Process intent parameters, if any.
        intent.getStringExtra("peer-bluetooth-address")?.let {
            appViewModel.peerBluetoothAddress = it
        }
        val packetCount = intent.getIntExtra("packet-count", 0)
        if (packetCount > 0) {
            appViewModel.senderPacketCount = packetCount
        }
        appViewModel.updateSenderPacketCountSlider()
        val packetSize = intent.getIntExtra("packet-size", 0)
        if (packetSize > 0) {
            appViewModel.senderPacketSize = packetSize
        }
        val packetInterval = intent.getIntExtra("packet-interval", 0)
        if (packetInterval > 0) {
            appViewModel.senderPacketInterval = packetInterval
        }
        appViewModel.updateSenderPacketSizeSlider()
        intent.getStringExtra("scenario")?.let {
            when (it) {
                "send" -> appViewModel.scenario = SEND_SCENARIO
                "receive" -> appViewModel.scenario = RECEIVE_SCENARIO
                "ping" -> appViewModel.scenario = PING_SCENARIO
                "pong" -> appViewModel.scenario = PONG_SCENARIO
            }
        }
        intent.getStringExtra("mode")?.let {
            when (it) {
                "rfcomm-client" -> appViewModel.mode = RFCOMM_CLIENT_MODE
                "rfcomm-server" -> appViewModel.mode = RFCOMM_SERVER_MODE
                "l2cap-client" -> appViewModel.mode = L2CAP_CLIENT_MODE
                "l2cap-server" -> appViewModel.mode = L2CAP_SERVER_MODE
            }
        }
        intent.getStringExtra("autostart")?.let {
            when (it) {
                "run-scenario" -> runScenario()
                "scan-start" -> runScan(true)
                "stop-start" -> runScan(false)
            }
        }
    }

    private fun runScenario() {
        if (bluetoothAdapter == null) {
            return
        }

        val runner = when (appViewModel.mode) {
            RFCOMM_CLIENT_MODE -> RfcommClient(appViewModel, bluetoothAdapter!!, ::createIoClient)
            RFCOMM_SERVER_MODE -> RfcommServer(appViewModel, bluetoothAdapter!!, ::createIoClient)
            L2CAP_CLIENT_MODE -> L2capClient(
                appViewModel,
                bluetoothAdapter!!,
                baseContext,
                ::createIoClient
            )
            L2CAP_SERVER_MODE -> L2capServer(appViewModel, bluetoothAdapter!!, ::createIoClient)
            else -> throw IllegalStateException()
        }
        runner.run()
    }

    private fun runScan(startScan: Boolean) {
        val scan = bluetoothAdapter?.let { Scan(it) }
        scan?.run(startScan)
    }

    private fun createIoClient(packetIo: PacketIO): IoClient {
        return when (appViewModel.scenario) {
            SEND_SCENARIO -> Sender(appViewModel, packetIo)
            RECEIVE_SCENARIO -> Receiver(appViewModel, packetIo)
            PING_SCENARIO -> Pinger(appViewModel, packetIo)
            PONG_SCENARIO -> Ponger(appViewModel, packetIo)
            else -> throw IllegalStateException()
        }
    }


    @SuppressLint("MissingPermission")
    fun becomeDiscoverable() {
        val discoverableIntent = Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
        discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300)
        startActivity(discoverableIntent)
    }
}

@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun MainView(
    appViewModel: AppViewModel,
    becomeDiscoverable: () -> Unit,
    runScenario: () -> Unit,
) {
    BTBenchTheme {
        val scrollState = rememberScrollState()
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState),
            color = MaterialTheme.colorScheme.background
        ) {
            Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                Text(
                    text = "Bumble Bench",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center
                )
                Divider()
                val keyboardController = LocalSoftwareKeyboardController.current
                val focusRequester = remember { FocusRequester() }
                val focusManager = LocalFocusManager.current
                TextField(
                    label = {
                        Text(text = "Peer Bluetooth Address")
                    },
                    value = appViewModel.peerBluetoothAddress,
                    modifier = Modifier
                        .fillMaxWidth()
                        .focusRequester(focusRequester),
                    keyboardOptions = KeyboardOptions.Default.copy(
                        keyboardType = KeyboardType.Ascii, imeAction = ImeAction.Done
                    ),
                    onValueChange = {
                        appViewModel.updatePeerBluetoothAddress(it)
                    },
                    keyboardActions = KeyboardActions(onDone = {
                        keyboardController?.hide()
                        focusManager.clearFocus()
                    }),
                    enabled = (appViewModel.mode == RFCOMM_CLIENT_MODE) or (appViewModel.mode == L2CAP_CLIENT_MODE)
                )
                Divider()
                TextField(
                    label = {
                        Text(text = "L2CAP PSM")
                    },
                    value = appViewModel.l2capPsm.toString(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .focusRequester(focusRequester),
                    keyboardOptions = KeyboardOptions.Default.copy(
                        keyboardType = KeyboardType.Number, imeAction = ImeAction.Done
                    ),
                    onValueChange = {
                        if (it.isNotEmpty()) {
                            val psm = it.toIntOrNull()
                            if (psm != null) {
                                appViewModel.l2capPsm = psm
                            }
                        }
                    },
                    keyboardActions = KeyboardActions(onDone = {
                        keyboardController?.hide()
                        focusManager.clearFocus()
                    }),
                    enabled = (appViewModel.mode == L2CAP_CLIENT_MODE)
                )
                Divider()
                Slider(
                    value = appViewModel.senderPacketCountSlider, onValueChange = {
                        appViewModel.senderPacketCountSlider = it
                        appViewModel.updateSenderPacketCount()
                    }, steps = 4
                )
                Text(text = "Packet Count: " + appViewModel.senderPacketCount.toString())
                Divider()
                Slider(
                    value = appViewModel.senderPacketSizeSlider, onValueChange = {
                        appViewModel.senderPacketSizeSlider = it
                        appViewModel.updateSenderPacketSize()
                    }, steps = 4
                )
                Text(text = "Packet Size: " + appViewModel.senderPacketSize.toString())
                Divider()
                TextField(
                    label = {
                        Text(text = "Packet Interval (ms)")
                    },
                    value = appViewModel.senderPacketInterval.toString(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .focusRequester(focusRequester),
                    keyboardOptions = KeyboardOptions.Default.copy(
                        keyboardType = KeyboardType.Number, imeAction = ImeAction.Done
                    ),
                    onValueChange = {
                        if (it.isNotEmpty()) {
                            val interval = it.toIntOrNull()
                            if (interval != null) {
                                appViewModel.updateSenderPacketInterval(interval)
                            }
                        }
                    },
                    keyboardActions = KeyboardActions(onDone = {
                        keyboardController?.hide()
                        focusManager.clearFocus()
                    }),
                    enabled = (appViewModel.scenario == PING_SCENARIO)
                )
                Divider()
                ActionButton(
                    text = "Become Discoverable", onClick = becomeDiscoverable, true
                )
                Row(
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(text = "2M PHY")
                    Spacer(modifier = Modifier.padding(start = 8.dp))
                    Switch(
                        enabled = (appViewModel.mode == L2CAP_CLIENT_MODE || appViewModel.mode == L2CAP_SERVER_MODE),
                        checked = appViewModel.use2mPhy,
                        onCheckedChange = { appViewModel.use2mPhy = it }
                    )

                }
                Row {
                    Column(Modifier.selectableGroup()) {
                        listOf(
                            RFCOMM_CLIENT_MODE,
                            RFCOMM_SERVER_MODE,
                            L2CAP_CLIENT_MODE,
                            L2CAP_SERVER_MODE
                        ).forEach { text ->
                            Row(
                                Modifier
                                    .selectable(
                                        selected = (text == appViewModel.mode),
                                        onClick = { appViewModel.updateMode(text) },
                                        role = Role.RadioButton
                                    )
                                    .padding(horizontal = 16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                RadioButton(
                                    selected = (text == appViewModel.mode),
                                    onClick = null
                                )
                                Text(
                                    text = text,
                                    style = MaterialTheme.typography.bodyLarge,
                                    modifier = Modifier.padding(start = 16.dp)
                                )
                            }
                        }
                    }
                    Column(Modifier.selectableGroup()) {
                        listOf(
                            SEND_SCENARIO,
                            RECEIVE_SCENARIO,
                            PING_SCENARIO,
                            PONG_SCENARIO
                        ).forEach { text ->
                            Row(
                                Modifier
                                    .selectable(
                                        selected = (text == appViewModel.scenario),
                                        onClick = { appViewModel.updateScenario(text) },
                                        role = Role.RadioButton
                                    )
                                    .padding(horizontal = 16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                RadioButton(
                                    selected = (text == appViewModel.scenario),
                                    onClick = null
                                )
                                Text(
                                    text = text,
                                    style = MaterialTheme.typography.bodyLarge,
                                    modifier = Modifier.padding(start = 16.dp)
                                )
                            }
                        }
                    }
                }
                Row {
                    ActionButton(
                        text = "Start", onClick = runScenario, enabled = !appViewModel.running
                    )
                    ActionButton(
                        text = "Stop", onClick = appViewModel::abort, enabled = appViewModel.running
                    )
                }
                Divider()
                Text(
                    text = if (appViewModel.mtu != 0) "MTU: ${appViewModel.mtu}" else ""
                )
                Text(
                    text = if (appViewModel.rxPhy != 0 || appViewModel.txPhy != 0) "PHY: tx=${appViewModel.txPhy}, rx=${appViewModel.rxPhy}" else ""
                )
                Text(
                    text = "Status: ${appViewModel.status}"
                )
                Text(
                    text = "Last Error: ${appViewModel.lastError}"
                )
                Text(
                    text = "Packets Sent: ${appViewModel.packetsSent}"
                )
                Text(
                    text = "Packets Received: ${appViewModel.packetsReceived}"
                )
                Text(
                    text = "Throughput: ${appViewModel.throughput}"
                )
                Text(
                    text = "Stats: ${appViewModel.stats}"
                )
            }
        }
    }
}

@Composable
fun ActionButton(text: String, onClick: () -> Unit, enabled: Boolean) {
    Button(onClick = onClick, enabled = enabled) {
        Text(text = text)
    }
}
