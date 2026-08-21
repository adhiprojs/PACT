package org.humanitarian.fieldapp.ui.theme

import android.app.Activity
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val PactColorScheme = lightColorScheme(
    primary = PactPrimary,
    onPrimary = PactOnPrimary,
    background = PactBackground,
    onBackground = PactTextPrimary,
    surface = PactSurface,
    onSurface = PactTextPrimary,
    surfaceVariant = PactAccent,
    onSurfaceVariant = PactTextSecondary,
    outline = PactAccent,
    error = PactPrimary,
    onError = Color.White
)

@Composable
fun PactTheme(
    content: @Composable () -> Unit
) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val activity = view.context as? Activity
            if (activity != null) {
                val window = activity.window
                window.statusBarColor = PactBackground.toArgb()
                window.navigationBarColor = PactBackground.toArgb()
                val controller = WindowCompat.getInsetsController(window, view)
                controller.isAppearanceLightStatusBars = true
                controller.isAppearanceLightNavigationBars = true
            }
        }
    }

    MaterialTheme(
        colorScheme = PactColorScheme,
        content = content
    )
}