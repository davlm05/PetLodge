package com.example.petlodge

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.ReservationResponse
import com.example.petlodge.databinding.ActivityMisReservasBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.util.Locale

class MisReservasActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMisReservasBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMisReservasBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToMain.setOnClickListener {
            finish()
        }

        binding.btnCrearReserva.setOnClickListener {
            startActivity(Intent(this, CrearReservaActivity::class.java))
        }
    }

    override fun onResume() {
        super.onResume()
        loadReservations()
    }

    private fun loadReservations() {
        setLoading(true)
        ApiClient.service.getReservations()
            .enqueue(object : Callback<ApiResponse<List<ReservationResponse>>> {
                override fun onResponse(
                    call: Call<ApiResponse<List<ReservationResponse>>>,
                    response: Response<ApiResponse<List<ReservationResponse>>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        renderReservations(body.data.orEmpty())
                    } else {
                        renderReservations(emptyList())
                        Toast.makeText(
                            this@MisReservasActivity,
                            body?.error ?: "Error al cargar las reservas.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<List<ReservationResponse>>>,
                    throwable: Throwable
                ) {
                    setLoading(false)
                    renderReservations(emptyList())
                    Toast.makeText(
                        this@MisReservasActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
    }

    private fun renderReservations(reservations: List<ReservationResponse>) {
        binding.reservationsContainer.removeAllViews()
        binding.tvEmptyState.visibility = if (reservations.isEmpty()) View.VISIBLE else View.GONE

        reservations.forEach { reservation ->
            binding.reservationsContainer.addView(createReservationCard(reservation))
        }
    }

    private fun createReservationCard(reservation: ReservationResponse): View {
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

        card.addView(createTextView(reservation.pet?.name ?: "Reserva #${reservation.id}", 18f, true))
        card.addView(
            createTextView(
                "Estado: ${reservation.status.toDisplayValue()}",
                14f,
                false,
                statusColor(reservation.status)
            )
        )
        card.addView(
            createTextView(
                "Fechas: ${reservation.checkInDate} a ${reservation.checkOutDate}",
                14f
            )
        )
        card.addView(
            createTextView(
                "Habitación: ${reservation.room?.number ?: reservation.roomId} (${reservation.lodgingType.toDisplayValue()})",
                14f
            )
        )

        val serviceNames = reservation.services.orEmpty()
            .mapNotNull { service -> service.serviceName }
            .takeIf { it.isNotEmpty() }
            ?.joinToString(", ")
            ?: "Sin servicios adicionales"
        card.addView(createTextView("Servicios: $serviceNames", 14f))

        reservation.notes?.takeIf { it.isNotBlank() }?.let { notes ->
            card.addView(createTextView("Notas: $notes", 14f))
        }

        card.addView(
            createTextView(
                "Total: ${formatCurrency(reservation.totalPrice ?: 0.0)}",
                15f,
                true
            )
        )

        if (reservation.status in listOf("confirmed", "in_progress")) {
            val cancelButton = Button(this).apply {
                text = "Cancelar reserva"
                backgroundTintList = ColorStateList.valueOf(getColor(R.color.danger))
                setTextColor(getColor(R.color.white))
                setOnClickListener { cancelReservation(reservation.id) }
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    dp(48)
                ).apply {
                    topMargin = dp(10)
                }
            }
            card.addView(cancelButton)
        }

        return card
    }

    private fun cancelReservation(reservationId: Int) {
        setLoading(true)
        ApiClient.service.cancelReservation(reservationId)
            .enqueue(object : Callback<ApiResponse<ReservationResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<ReservationResponse>>,
                    response: Response<ApiResponse<ReservationResponse>>
                ) {
                    setLoading(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@MisReservasActivity,
                            body.message ?: "Reserva cancelada.",
                            Toast.LENGTH_LONG
                        ).show()
                        loadReservations()
                    } else {
                        Toast.makeText(
                            this@MisReservasActivity,
                            body?.error ?: "Error al cancelar la reserva.",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<ReservationResponse>>,
                    throwable: Throwable
                ) {
                    setLoading(false)
                    Toast.makeText(
                        this@MisReservasActivity,
                        "Error al conectar con el servidor.",
                        Toast.LENGTH_LONG
                    ).show()
                }
            })
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
        binding.btnCrearReserva.isEnabled = !isLoading
    }

    private fun statusColor(status: String): Int = when (status) {
        "confirmed" -> getColor(R.color.success)
        "in_progress" -> getColor(R.color.warning)
        "cancelled" -> getColor(R.color.danger)
        else -> getColor(R.color.text_light)
    }

    private fun formatCurrency(value: Double): String =
        "CRC ${String.format(Locale.US, "%,.2f", value)}"

    private fun String.toDisplayValue(): String = when (this) {
        "standard" -> "Estándar"
        "special" -> "Especial"
        "confirmed" -> "Confirmada"
        "in_progress" -> "En progreso"
        "completed" -> "Completada"
        "cancelled" -> "Cancelada"
        else -> replaceFirstChar { character ->
            if (character.isLowerCase()) character.titlecase() else character.toString()
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()
}
