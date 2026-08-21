package org.humanitarian.fieldapp.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.humanitarian.fieldapp.models.UserSession
import org.humanitarian.fieldapp.offline.OfflineQueue
import org.humanitarian.fieldapp.sync.SyncManager
import org.humanitarian.fieldapp.ui.theme.PactAccent
import org.humanitarian.fieldapp.ui.theme.PactBackground
import org.humanitarian.fieldapp.ui.theme.PactOnPrimary
import org.humanitarian.fieldapp.ui.theme.PactPrimary
import org.humanitarian.fieldapp.ui.theme.PactSurface
import org.humanitarian.fieldapp.ui.theme.PactTextPrimary
import org.humanitarian.fieldapp.ui.theme.PactTextSecondary

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onNavigateToFieldReport: () -> Unit,
    onNavigateToMyRequests: () -> Unit,
    onNavigateToSmsFallback: () -> Unit,
    onNavigateToSmsDecoder: () -> Unit,
    onNavigateToOfflineMap: () -> Unit,
    onNavigateToStatus: () -> Unit,
    onLogout: () -> Unit
) {
    val context = LocalContext.current
    val userProfile = remember { UserSession.getUser(context) }
    var queueSize by remember { mutableStateOf(OfflineQueue.getQueueSize(context)) }
    var autoSyncMessage by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        queueSize = OfflineQueue.getQueueSize(context)
        if (queueSize > 0) {
            val result = SyncManager.syncQueue(context)
            if (result.synced > 0) {
                autoSyncMessage = "${result.synced} queued report(s) synced automatically."
            }
            queueSize = OfflineQueue.getQueueSize(context)
        }
    }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = "PACT Field App",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color = PactTextPrimary
                        )
                        Text(
                            text = "${userProfile.displayName} · ${userProfile.organizationId}",
                            style = MaterialTheme.typography.bodySmall,
                            color = PactTextSecondary
                        )
                    }
                },
                actions = {
                    Text(
                        text = "Logout",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold,
                        color = PactPrimary,
                        modifier = Modifier
                            .clickable {
                                UserSession.logout(context)
                                onLogout()
                            }
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PactSurface,
                    titleContentColor = PactTextPrimary
                )
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
            // CARD 1: LOGGED IN AS PROFILE CARD
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 20.dp, vertical = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(
                            text = "Logged in as",
                            style = MaterialTheme.typography.bodySmall,
                            color = PactTextSecondary
                        )
                        Text(
                            text = userProfile.roleTitle,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = PactTextPrimary
                        )
                    }

                    // Organization ID Badge
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = PactAccent,
                        border = BorderStroke(1.dp, PactAccent)
                    ) {
                        Text(
                            text = userProfile.organizationId,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            color = PactPrimary,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                        )
                    }
                }
            }

            // CARD 2: MISSION CONSOLE DESCRIPTION
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = "Mission Console",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = PactTextPrimary
                    )
                    Text(
                        text = "Select an operational module. The interface is optimized for low connectivity and fast field use.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = PactTextSecondary
                    )
                }
            }

            // CARD 3: OFFLINE QUEUE BANNER (When reports exist)
            if (queueSize > 0) {
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onNavigateToMyRequests() },
                    shape = RoundedCornerShape(18.dp),
                    color = PactSurface,
                    border = BorderStroke(1.5.dp, PactPrimary)
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Text(
                            text = "$queueSize report(s) in offline queue",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = PactTextPrimary
                        )
                        Text(
                            text = "Open My Requests to view payloads or sync when internet returns.",
                            style = MaterialTheme.typography.bodySmall,
                            color = PactTextSecondary
                        )
                    }
                }
            }

            // MENU BUTTONS LIST (Exact order from screenshot)

            // 1. Field Report (Filled Red Button)
            Button(
                onClick = onNavigateToFieldReport,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PactPrimary,
                    contentColor = PactOnPrimary
                )
            ) {
                Text(
                    text = "Field Report",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
            }

            // 2. Dynamic Requests / Assigned Missions Button
            val isDonor = userProfile.roleKey.equals("donor", ignoreCase = true) || userProfile.roleKey.equals("admin", ignoreCase = true)
            SurfaceMenuButton(
                title = if (isDonor) "Assigned Relief Missions" else "My Requests",
                onClick = onNavigateToMyRequests
            )

            // 3. SMS Gateway Hub (Surface Button)
            SurfaceMenuButton(
                title = "SMS Gateway Hub",
                onClick = onNavigateToSmsDecoder
            )

            // 4. SMS Fallback (Surface Button)
            SurfaceMenuButton(
                title = "SMS Fallback",
                onClick = onNavigateToSmsFallback
            )

            // 5. Offline Map (Surface Button)
            SurfaceMenuButton(
                title = "Offline Map",
                onClick = onNavigateToOfflineMap
            )
        }
    }
}

@Composable
fun SurfaceMenuButton(
    title: String,
    onClick: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .height(54.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        color = PactSurface,
        border = BorderStroke(1.dp, PactAccent)
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = PactTextPrimary
            )
        }
    }
}