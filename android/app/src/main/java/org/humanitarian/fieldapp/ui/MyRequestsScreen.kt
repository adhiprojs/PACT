package org.humanitarian.fieldapp.ui

import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import org.humanitarian.fieldapp.models.OrgRequest
import org.humanitarian.fieldapp.models.UserSession
import org.humanitarian.fieldapp.network.ApiClient
import org.humanitarian.fieldapp.network.ApiResult
import org.humanitarian.fieldapp.ui.theme.*

private fun statusColor(status: String): Color {
    return when (status.lowercase()) {
        "pending" -> Color(0xFFFF9800)                                                  // orange
        "accepted", "processing", "matched", "allocated", "in_transit", "intransit" -> Color(0xFF2196F3) // blue
        "completed", "delivered", "verified" -> Color(0xFF4CAF50)                       // green
        "rejected", "duplicate", "denied" -> Color(0xFFF62440)                          // red
        else -> Color(0xFF7C6A58)
    }
}

private fun statusLabel(status: String): String {
    return when (status.lowercase()) {
        "pending" -> "PENDING REVIEW"
        "accepted", "allocated" -> "ALLOCATED · READY"
        "processing" -> "PROCESSING"
        "matched" -> "RESOURCES MATCHED"
        "in_transit", "intransit" -> "IN TRANSIT · EN ROUTE"
        "completed", "delivered" -> "DELIVERED · COMPLETED"
        "rejected", "denied" -> "DENIED"
        "duplicate" -> "DUPLICATE"
        else -> status.uppercase()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyRequestsScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val userProfile = remember { UserSession.getUser(context) }
    val isDonor = remember { userProfile.roleKey.equals("donor", ignoreCase = true) || userProfile.roleKey.equals("admin", ignoreCase = true) }

    var requests by remember { mutableStateOf<List<OrgRequest>>(emptyList()) }
    var lastSync by remember { mutableStateOf("Loading…") }

    // Poll status every 3 seconds
    LaunchedEffect(Unit) {
        while (true) {
            val res = if (isDonor) {
                ApiClient.getAssignedMissionsForDonor(userProfile.organizationId)
            } else {
                ApiClient.getRequestsByOrg(userProfile.organizationId)
            }

            when (res) {
                is ApiResult.Success -> {
                    requests = res.data
                    lastSync = if (isDonor) "Live · synced with Command Center" else "Live · synced with coordinator"
                }
                is ApiResult.Error -> lastSync = "Backend unreachable"
            }
            delay(3000)
        }
    }

    val pageTitle = if (isDonor) "Assigned Missions" else "My Requests"

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = { Text(pageTitle, fontWeight = FontWeight.SemiBold, color = PactTextPrimary) },
                navigationIcon = { TextButton(onClick = onBack) { Text("Back", color = PactPrimary, fontWeight = FontWeight.SemiBold) } },
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
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(lastSync, style = MaterialTheme.typography.bodySmall, color = PactTextSecondary)

            if (requests.isEmpty()) {
                val emptyText = if (isDonor) {
                    "No missions assigned to ${userProfile.organizationId} yet. As soon as emergencies occur in your sector, allocations will appear here."
                } else {
                    "No requests submitted yet by ${userProfile.organizationId}."
                }
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    color = PactSurface,
                    border = BorderStroke(1.dp, PactAccent)
                ) {
                    Text(emptyText, style = MaterialTheme.typography.bodyMedium, color = PactTextSecondary, modifier = Modifier.padding(20.dp))
                }
            }

            requests.forEach { req ->
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    color = PactSurface,
                    border = BorderStroke(1.dp, PactAccent)
                ) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = req.id,
                                fontWeight = FontWeight.Bold,
                                color = PactTextPrimary,
                                style = MaterialTheme.typography.titleMedium
                            )
                            Text(
                                text = statusLabel(req.status),
                                style = MaterialTheme.typography.labelMedium,
                                fontWeight = FontWeight.Bold,
                                color = statusColor(req.status)
                            )
                        }

                        if (isDonor) {
                            // Donor Group Mission Details
                            Text(
                                text = "Mission: Deliver ${req.resource}",
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = PactTextPrimary
                            )

                            Surface(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp),
                                color = PactAccent.copy(alpha = 0.45f),
                                border = BorderStroke(1.dp, PactPrimary.copy(alpha = 0.25f))
                            ) {
                                Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                    Text(
                                        text = "DISPATCH CARGO INSTRUCTIONS",
                                        style = MaterialTheme.typography.labelSmall,
                                        fontWeight = FontWeight.Bold,
                                        color = PactPrimary
                                    )
                                    Text(
                                        text = "Release Stock: ${req.allocatedCargo ?: req.resource}",
                                        style = MaterialTheme.typography.bodyMedium,
                                        fontWeight = FontWeight.Bold,
                                        color = PactTextPrimary
                                    )
                                    Text(
                                        text = "Target ETA: ~${req.etaHours ?: 1.0}h to destination",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = PactTextSecondary
                                    )
                                }
                            }

                            // Action buttons for Donor to update delivery status
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Button(
                                    onClick = {
                                        coroutineScope.launch {
                                            val res = ApiClient.updateMissionStatus(req.id, "1", "In Transit")
                                            if (res is ApiResult.Success) {
                                                Toast.makeText(context, "Dispatched: In Transit", Toast.LENGTH_SHORT).show()
                                            }
                                        }
                                    },
                                    modifier = Modifier.weight(1f),
                                    shape = RoundedCornerShape(10.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = PactPrimary, contentColor = PactOnPrimary)
                                ) {
                                    Text("Start Transit", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelMedium)
                                }

                                OutlinedButton(
                                    onClick = {
                                        coroutineScope.launch {
                                            val res = ApiClient.updateMissionStatus(req.id, "2", "Delivered")
                                            if (res is ApiResult.Success) {
                                                Toast.makeText(context, "Confirmed: Delivered", Toast.LENGTH_SHORT).show()
                                            }
                                        }
                                    },
                                    modifier = Modifier.weight(1f),
                                    shape = RoundedCornerShape(10.dp),
                                    border = BorderStroke(1.dp, Color(0xFF4CAF50)),
                                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF2E7D32))
                                ) {
                                    Text("Delivered", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelMedium)
                                }
                            }
                        } else {
                            // Individual / Requester View
                            Text(
                                text = "${req.type.uppercase()} · ${req.resource} × ${req.quantity}",
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = PactTextPrimary
                            )

                            if (!req.allocatedProvider.isNullOrBlank()) {
                                Surface(
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(12.dp),
                                    color = PactAccent.copy(alpha = 0.5f),
                                    border = BorderStroke(1.dp, PactPrimary.copy(alpha = 0.25f))
                                ) {
                                    Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                        Text(
                                            text = "DISPATCHED HELPER / PROVIDER",
                                            style = MaterialTheme.typography.labelSmall,
                                            fontWeight = FontWeight.Bold,
                                            color = PactPrimary
                                        )
                                        Text(
                                            text = req.allocatedProvider,
                                            style = MaterialTheme.typography.titleSmall,
                                            fontWeight = FontWeight.Bold,
                                            color = PactTextPrimary
                                        )
                                        if (!req.allocatedCargo.isNullOrBlank()) {
                                            Text(
                                                text = "Supplying: ${req.allocatedCargo}",
                                                style = MaterialTheme.typography.bodySmall,
                                                fontWeight = FontWeight.Medium,
                                                color = PactTextPrimary
                                            )
                                        }
                                        if (req.etaHours != null && req.etaHours > 0) {
                                            Text(
                                                text = "Estimated Transit Arrival: ~${req.etaHours}h · Plan #${req.planId ?: ""}",
                                                style = MaterialTheme.typography.labelSmall,
                                                color = PactTextSecondary
                                            )
                                        }
                                    }
                                }
                            }
                        }

                        // GPS Coordinates
                        val coords = if (req.latitude != null && req.longitude != null)
                            String.format("Destination GPS: %.4f, %.4f", req.latitude, req.longitude)
                        else "GPS: not attached"

                        Text(
                            text = coords,
                            style = MaterialTheme.typography.bodySmall,
                            fontFamily = FontFamily.Monospace,
                            color = PactTextSecondary
                        )
                    }
                }
            }
        }
    }
}