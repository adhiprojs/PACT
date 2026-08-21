package org.humanitarian.fieldapp.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AdminPanelSettings
import androidx.compose.material.icons.filled.Group
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.humanitarian.fieldapp.models.UserProfile
import org.humanitarian.fieldapp.models.UserSession
import org.humanitarian.fieldapp.ui.theme.PactAccent
import org.humanitarian.fieldapp.ui.theme.PactBackground
import org.humanitarian.fieldapp.ui.theme.PactOnPrimary
import org.humanitarian.fieldapp.ui.theme.PactPrimary
import org.humanitarian.fieldapp.ui.theme.PactSurface
import org.humanitarian.fieldapp.ui.theme.PactTextPrimary
import org.humanitarian.fieldapp.ui.theme.PactTextSecondary

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit
) {
    val context = LocalContext.current
    var selectedRole by remember { mutableStateOf<String?>(null) }
    var displayName by remember { mutableStateOf("") }
    var organizationId by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = "Welcome to PACT",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = PactTextPrimary
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
            Text(
                text = "Select your role to continue",
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium,
                color = PactTextSecondary,
                modifier = Modifier.padding(bottom = 4.dp)
            )

            // Role 1: Administrator
            RoleSelectionCard(
                title = "Administrator",
                description = "Coordinate resources and manage the network",
                icon = Icons.Default.AdminPanelSettings,
                isSelected = selectedRole == "admin",
                onClick = {
                    selectedRole = "admin"
                    if (displayName.isBlank()) displayName = "Adhi"
                    if (organizationId.isBlank() || organizationId == "RADM12" || organizationId == "NGO01") {
                        organizationId = "ADMIN01"
                    }
                }
            )

            // Role 2: Donor Group
            RoleSelectionCard(
                title = "Donor Group",
                description = "Organization providing resources and aid",
                icon = Icons.Default.Group,
                isSelected = selectedRole == "donor",
                onClick = {
                    selectedRole = "donor"
                    if (displayName.isBlank()) displayName = "Red Cross TN"
                    if (organizationId.isBlank() || organizationId == "ADMIN01" || organizationId == "RADM12") {
                        organizationId = "NGO01"
                    }
                }
            )

            // Role 3: Individual
            RoleSelectionCard(
                title = "Individual",
                description = "Field worker or person in need of assistance",
                icon = Icons.Default.Person,
                isSelected = selectedRole == "individual",
                onClick = {
                    selectedRole = "individual"
                    if (displayName.isBlank()) displayName = "Adhi"
                    if (organizationId.isBlank() || organizationId == "ADMIN01" || organizationId == "NGO01") {
                        organizationId = "RADM12"
                    }
                }
            )

            // Role Setup Form Card (Appears below when a role is selected)
            if (selectedRole != null) {
                val roleTitle = when (selectedRole) {
                    "admin" -> "Admin Setup"
                    "donor" -> "Donor Group Setup"
                    else -> "Individual Setup"
                }
                val nameHint = when (selectedRole) {
                    "admin" -> "Your name as coordinator"
                    "donor" -> "Organization or group name"
                    else -> "Your name"
                }
                val orgHint = when (selectedRole) {
                    "admin" -> "Admin coordinator ID (e.g., ADMIN01)"
                    "donor" -> "Your organization ID (e.g., NGO01, CSR02)"
                    else -> "Your individual ID (e.g., WORKER01)"
                }

                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp),
                    shape = RoundedCornerShape(20.dp),
                    color = PactSurface,
                    border = BorderStroke(1.dp, PactAccent)
                ) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        Text(
                            text = roleTitle,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = PactTextPrimary
                        )

                        // Display Name
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            OutlinedTextField(
                                value = displayName,
                                onValueChange = {
                                    displayName = it
                                    errorMessage = ""
                                },
                                label = { Text("Display Name") },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = PactPrimary,
                                    unfocusedBorderColor = PactAccent,
                                    focusedLabelColor = PactPrimary,
                                    unfocusedLabelColor = PactTextSecondary,
                                    focusedTextColor = PactTextPrimary,
                                    unfocusedTextColor = PactTextPrimary,
                                    focusedContainerColor = Color.White,
                                    unfocusedContainerColor = Color.White
                                )
                            )
                            Text(
                                text = nameHint,
                                style = MaterialTheme.typography.labelSmall,
                                color = PactTextSecondary,
                                modifier = Modifier.padding(start = 4.dp)
                            )
                        }

                        // Organization ID
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            OutlinedTextField(
                                value = organizationId,
                                onValueChange = {
                                    organizationId = it.uppercase()
                                    errorMessage = ""
                                },
                                label = { Text("Organization ID") },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = PactPrimary,
                                    unfocusedBorderColor = PactAccent,
                                    focusedLabelColor = PactPrimary,
                                    unfocusedLabelColor = PactTextSecondary,
                                    focusedTextColor = PactTextPrimary,
                                    unfocusedTextColor = PactTextPrimary,
                                    focusedContainerColor = Color.White,
                                    unfocusedContainerColor = Color.White
                                )
                            )
                            Text(
                                text = orgHint,
                                style = MaterialTheme.typography.labelSmall,
                                color = PactTextSecondary,
                                modifier = Modifier.padding(start = 4.dp)
                            )
                        }

                        if (errorMessage.isNotBlank()) {
                            Text(
                                text = errorMessage,
                                style = MaterialTheme.typography.bodySmall,
                                color = PactPrimary
                            )
                        }

                        Spacer(modifier = Modifier.height(4.dp))

                        // Continue Button
                        Button(
                            onClick = {
                                val cleanName = displayName.trim()
                                val cleanOrg = organizationId.trim().uppercase()
                                if (cleanName.isBlank()) {
                                    errorMessage = "Please enter a display name"
                                    return@Button
                                }
                                if (cleanOrg.isBlank()) {
                                    errorMessage = "Please enter an organization or worker ID"
                                    return@Button
                                }

                                val finalTitle = when (selectedRole) {
                                    "admin" -> "Administrator"
                                    "donor" -> "Donor Group"
                                    else -> "Individual"
                                }

                                val profile = UserProfile(
                                    roleKey = selectedRole ?: "individual",
                                    roleTitle = finalTitle,
                                    displayName = cleanName,
                                    organizationId = cleanOrg
                                )
                                UserSession.saveUser(context, profile)
                                onLoginSuccess()
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(52.dp),
                            shape = RoundedCornerShape(16.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = PactPrimary,
                                contentColor = PactOnPrimary
                            )
                        ) {
                            Text(
                                text = "Continue",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun RoleSelectionCard(
    title: String,
    description: String,
    icon: ImageVector,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(18.dp),
        color = PactSurface,
        border = if (isSelected) {
            BorderStroke(2.dp, PactPrimary)
        } else {
            BorderStroke(1.dp, PactAccent)
        }
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Circular icon container
            Surface(
                modifier = Modifier.size(48.dp),
                shape = CircleShape,
                color = if (isSelected) PactPrimary else PactAccent
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = title,
                        tint = if (isSelected) Color.White else PactTextPrimary,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }

            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(2.dp)
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = PactTextPrimary
                )
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodySmall,
                    color = PactTextSecondary
                )
            }
        }
    }
}
