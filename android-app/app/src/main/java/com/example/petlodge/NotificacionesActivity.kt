package com.example.petlodge

import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.NotificationResponse
import com.example.petlodge.databinding.ActivityNotificacionesBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class NotificacionesActivity : AppCompatActivity() {
    private lateinit var binding: ActivityNotificacionesBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityNotificacionesBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToMain.setOnClickListener {
            finish()
        }
    }

    override fun onResume() {
        super.onResume()
        loadNotifications()
    }

    private fun loadNotifications() {
        setLoading(true)
        ApiClient.service.getNotifications()
            .enqueue(object : Callback<ApiResponse<List<NotificationResponse>>> {
                override fun onResponse(
                    call: Call<ApiResponse<List<NotificationResponse>>>,
                    response: Response<ApiResponse<List<NotificationResponse>>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        renderNotifications(body.data.orEmpty())
                    } else {
                        renderNotifications(emptyList())
                        Toast.makeText(
                            this@NotificacionesActivity,
                            body?.error ?: "Error al cargar las notificaciones.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<List<NotificationResponse>>>,
                    throwable: Throwable
                ) {
                    setLoading(false)
                    renderNotifications(emptyList())
                    Toast.makeText(
                        this@NotificacionesActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun renderNotifications(notifications: List<NotificationResponse>) {
        binding.notificationsContainer.removeAllViews()
        binding.tvEmptyState.visibility = if (notifications.isEmpty()) View.VISIBLE else View.GONE

        notifications.forEach { notification ->
            binding.notificationsContainer.addView(createNotificationCard(notification))
        }
    }

    private fun createNotificationCard(notification: NotificationResponse): View {
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), dp(14), dp(16), dp(14))
            background = GradientDrawable().apply {
                setColor(getColor(R.color.white))
                setStroke(dp(1), getColor(R.color.border_color))
                cornerRadius = dp(8).toFloat()
            }
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                bottomMargin = dp(12)
            }
        }

        card.addView(
            createTextView(
                notification.subject?.takeIf { it.isNotBlank() }
                    ?: notification.eventType.toDisplayValue(),
                17f,
                true
            )
        )
        card.addView(
            createTextView(
                "Estado: ${notification.status.toDisplayValue()}",
                14f,
                false,
                statusColor(notification.status)
            )
        )
        card.addView(
            createTextView(
                "Destinatario: ${notification.recipientEmail ?: "Sin correo"}",
                14f
            )
        )
        card.addView(
            createTextView(
                "Fecha: ${notification.sentAt ?: notification.createdAt ?: "Pendiente"}",
                14f
            )
        )
        notification.errorMessage?.takeIf { it.isNotBlank() }?.let { error ->
            card.addView(
                createTextView(
                    "Error: ${error.toNotificationErrorSummary()}",
                    14f,
                    false,
                    getColor(R.color.danger)
                )
            )
        }

        return card
    }

    private fun createTextView(
        value: String,
        textSizeSp: Float,
        bold: Boolean = false,
        color: Int = getColor(R.color.text_dark)
    ): TextView = TextView(this).apply {
        text = value
        textSize = textSizeSp
        setTextColor(color)
        if (bold) {
            setTypeface(typeface, android.graphics.Typeface.BOLD)
        }
        layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply {
            bottomMargin = dp(6)
        }
    }

    private fun setLoading(isLoading: Boolean) {
        binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
    }

    private fun statusColor(status: String): Int = when (status) {
        "sent" -> getColor(R.color.success)
        "failed" -> getColor(R.color.danger)
        else -> getColor(R.color.text_light)
    }

    private fun String.toDisplayValue(): String = when (this) {
        "user_registered" -> "Registro de usuario"
        "reservation_confirmed" -> "Reserva confirmada"
        "reservation_modified" -> "Reserva modificada"
        "lodging_started" -> "Hospedaje iniciado"
        "lodging_ended" -> "Hospedaje finalizado"
        "pet_status_notice" -> "Aviso de mascota"
        "sent" -> "Enviada"
        "failed" -> "Fallida"
        "pending" -> "Pendiente"
        else -> replace("_", " ").replaceFirstChar { character ->
            if (character.isLowerCase()) character.titlecase() else character.toString()
        }
    }

    private fun String.toNotificationErrorSummary(): String {
        val normalized = replace("\n", " ").trim()
        return when {
            normalized.contains("Authentication Required", ignoreCase = true) ->
                "Autenticación SMTP requerida."
            normalized.length > 120 -> normalized.take(117) + "..."
            else -> normalized
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()
}
