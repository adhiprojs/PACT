package org.humanitarian.fieldapp.ui

import android.content.Intent
import android.net.Uri
import android.telephony.SmsManager
import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import org.humanitarian.fieldapp.network.ApiClient
import org.humanitarian.fieldapp.network.ApiResult
import org.humanitarian.fieldapp.offline.OfflineQueue
import org.humanitarian.fieldapp.ui.theme.*

const val PACT_GATEWAY_PHONE = "9345302551"

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SmsFallbackScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    val coroutineScope = rememberCoroutineScope()
    
    var queuedPayloads by remember { mutableStateOf<List<String>>(emptyList()) }
    var statusMessage by remember { mutableStateOf("") }

    fun refreshQueue() {
        val reports = OfflineQueue.getQueuedReports(context)
        queuedPayloads = reports.map { it.smsPayload }.filter { it.isNotBlank() }
    }

    LaunchedEffect(Unit) {
        refreshQueue()
    }

    fun dispatchSms(payload: String) {
        val success = org.humanitarian.fieldapp.sms.DirectSmsSender.sendDirectSms(context, PACT_GATEWAY_PHONE, payload)
        if (success) {
            Toast.makeText(context, "SMS dispatched to $PACT_GATEWAY_PHONE", Toast.LENGTH_LONG).show()
            statusMessage = "Dispatched SMS directly to $PACT_GATEWAY_PHONE via Cellular SIM."
        } else {
            val intent = Intent(Intent.ACTION_SENDTO).apply {
                data = Uri.parse("smsto:$PACT_GATEWAY_PHONE")
                putExtra("sms_body", payload)
            }
            context.startActivity(intent)
            statusMessage = "Opened SMS Messenger for $PACT_GATEWAY_PHONE."
        }
    }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = { Text("SMS Fallback Queue", fontWeight = FontWeight.SemiBold, color = PactTextPrimary) },
                navigationIcon = { TextButton(onClick = onBack) { Text("Back", color = PactPrimary) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PactSurface)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Gateway Target: $PACT_GATEWAY_PHONE", fontWeight = FontWeight.Bold, color = PactTextPrimary)
                    Text("Messages are sent directly over GSM cellular SMS to your Termux gateway laptop bridge.", color = PactTextSecondary, style = MaterialTheme.typography.bodySmall)
                }
            }

            if (queuedPayloads.isEmpty()) {
                Text("No pending SMS reports in queue.", color = PactTextSecondary)
            } else {
                Text("Pending Reports: ${queuedPayloads.size}", style = MaterialTheme.typography.titleMedium, color = PactTextPrimary)
                
                for ((index, payload) in queuedPayloads.withIndex()) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        color = PactSurface,
                        border = BorderStroke(1.dp, PactAccent)
                    ) {
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("Report #${index + 1}", fontWeight = FontWeight.Bold, color = PactTextPrimary)
                            
                            Text(
                                text = payload,
                                fontFamily = FontFamily.Monospace,
                                color = PactPrimary,
                                modifier = Modifier.fillMaxWidth()
                            )

                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Button(
                                    onClick = { dispatchSms(payload) },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = ButtonDefaults.buttonColors(containerColor = PactPrimary, contentColor = PactOnPrimary)
                                ) { 
                                    Text("📱 Send Cellular SMS ($PACT_GATEWAY_PHONE)") 
                                }

                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    OutlinedButton(
                                        onClick = { 
                                            clipboardManager.setText(AnnotatedString(payload))
                                            Toast.makeText(context, "Copied payload", Toast.LENGTH_SHORT).show()
                                        },
                                        modifier = Modifier.weight(1f),
                                        colors = ButtonDefaults.outlinedButtonColors(contentColor = PactTextPrimary)
                                    ) { Text("Copy") }

                                    Button(
                                        onClick = {
                                            coroutineScope.launch {
                                                statusMessage = "Sending via HTTP Gateway API..."
                                                when (val result = ApiClient.postSmsWebhook(payload)) {
                                                    is ApiResult.Success -> {
                                                        statusMessage = "Success! Ingested by backend."
                                                    }
                                                    is ApiResult.Error -> {
                                                        statusMessage = "HTTP Failed: ${result.message}"
                                                    }
                                                }
                                            }
                                        },
                                        modifier = Modifier.weight(1f),
                                        colors = ButtonDefaults.buttonColors(containerColor = PactAccent, contentColor = PactTextPrimary)
                                    ) { Text("HTTP Bridge") }
                                }
                            }
                        }
                    }
                }
            }
            
            if (statusMessage.isNotBlank()) {
                Text(statusMessage, color = PactPrimary, fontWeight = FontWeight.Bold)
            }
        }
    }
}