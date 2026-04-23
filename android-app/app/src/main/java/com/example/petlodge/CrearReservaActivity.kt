package com.example.petlodge

import android.app.DatePickerDialog
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.CheckBox
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.petlodge.data.ApiClient
import com.example.petlodge.data.dto.ApiResponse
import com.example.petlodge.data.dto.PetResponse
import com.example.petlodge.data.dto.ReservationCreateRequest
import com.example.petlodge.data.dto.ReservationResponse
import com.example.petlodge.data.dto.RoomResponse
import com.example.petlodge.data.dto.ServiceResponse
import com.example.petlodge.databinding.ActivityCrearReservaBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale
import java.util.concurrent.TimeUnit

class CrearReservaActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCrearReservaBinding

    private val pets = mutableListOf<PetResponse>()
    private val rooms = mutableListOf<RoomResponse>()
    private val services = mutableListOf<ServiceResponse>()
    private val serviceChecks = linkedMapOf<Int, CheckBox>()
    private var pendingCatalogLoads = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCrearReservaBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnBackToReservas.setOnClickListener {
            finish()
        }

        binding.spinnerHabitacion.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                updateLodgingType()
                updateTotal()
            }

            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }

        val totalWatcher = object : TextWatcher {
            override fun beforeTextChanged(text: CharSequence?, start: Int, count: Int, after: Int) = Unit

            override fun onTextChanged(text: CharSequence?, start: Int, before: Int, count: Int) {
                updateTotal()
            }

            override fun afterTextChanged(editable: Editable?) = Unit
        }
        binding.etFechaIngreso.addTextChangedListener(totalWatcher)
        binding.etFechaSalida.addTextChangedListener(totalWatcher)
        setupDatePickerFields()

        binding.btnVerificarDisponibilidad.setOnClickListener {
            updateTotal()
            Toast.makeText(
                this,
                "La disponibilidad se valida al confirmar la reserva.",
                Toast.LENGTH_LONG
            ).show()
        }

        binding.btnSave.setOnClickListener {
            submitReservation()
        }

        loadCatalogData()
    }

    private fun setupDatePickerFields() {
        val tomorrow = Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR, 1) }
        val dayAfterTomorrow = Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR, 2) }

        binding.etFechaIngreso.apply {
            isFocusable = false
            isCursorVisible = false
            setText(outputDateFormat.format(tomorrow.time))
            setOnClickListener {
                showDatePicker(parseDateInput(text.toString()) ?: tomorrow.time) { selectedDate ->
                    setText(outputDateFormat.format(selectedDate))
                    val checkOut = parseDateInput(binding.etFechaSalida.text.toString())
                    if (checkOut == null || daysBetween(selectedDate, checkOut) <= 0) {
                        binding.etFechaSalida.setText(
                            outputDateFormat.format(datePlusDays(selectedDate, 1))
                        )
                    }
                    updateTotal()
                }
            }
        }

        binding.etFechaSalida.apply {
            isFocusable = false
            isCursorVisible = false
            setText(outputDateFormat.format(dayAfterTomorrow.time))
            setOnClickListener {
                val checkIn = parseDateInput(binding.etFechaIngreso.text.toString())
                val minCheckOutDate = checkIn?.let { datePlusDays(it, 1) } ?: tomorrow.time
                val currentCheckOut = parseDateInput(text.toString())
                showDatePicker(
                    defaultDate = currentCheckOut?.takeIf { !it.before(minCheckOutDate) }
                        ?: minCheckOutDate,
                    minDate = minCheckOutDate
                ) { selectedDate ->
                    setText(outputDateFormat.format(selectedDate))
                    updateTotal()
                }
            }
        }
    }

    private fun showDatePicker(
        defaultDate: Date,
        minDate: Date = Calendar.getInstance().time,
        onDateSelected: (Date) -> Unit
    ) {
        val calendar = Calendar.getInstance().apply { time = defaultDate }
        DatePickerDialog(
            this,
            { _, year, month, dayOfMonth ->
                val selected = Calendar.getInstance().apply {
                    set(year, month, dayOfMonth, 0, 0, 0)
                    set(Calendar.MILLISECOND, 0)
                }
                onDateSelected(selected.time)
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        ).apply {
            datePicker.minDate = minDate.atStartOfDay().time
        }.show()
    }

    private fun loadCatalogData() {
        pendingCatalogLoads = 3
        setLoading(true)
        loadPets()
        loadRooms()
        loadServices()
    }

    private fun loadPets() {
        ApiClient.service.getPets().enqueue(object : Callback<ApiResponse<List<PetResponse>>> {
            override fun onResponse(
                call: Call<ApiResponse<List<PetResponse>>>,
                response: Response<ApiResponse<List<PetResponse>>>
            ) {
                val body = response.body()
                if (response.isSuccessful && body?.success == true) {
                    pets.clear()
                    pets.addAll(body.data.orEmpty())
                    bindPets()
                } else {
                    showServerError(body?.error, "Error al cargar las mascotas.")
                }
                markCatalogLoadFinished()
            }

            override fun onFailure(call: Call<ApiResponse<List<PetResponse>>>, throwable: Throwable) {
                showConnectionError()
                markCatalogLoadFinished()
            }
        })
    }

    private fun loadRooms() {
        ApiClient.service.getRooms().enqueue(object : Callback<ApiResponse<List<RoomResponse>>> {
            override fun onResponse(
                call: Call<ApiResponse<List<RoomResponse>>>,
                response: Response<ApiResponse<List<RoomResponse>>>
            ) {
                val body = response.body()
                if (response.isSuccessful && body?.success == true) {
                    rooms.clear()
                    rooms.addAll(body.data.orEmpty())
                    bindRooms()
                } else {
                    showServerError(body?.error, "Error al cargar las habitaciones.")
                }
                markCatalogLoadFinished()
            }

            override fun onFailure(call: Call<ApiResponse<List<RoomResponse>>>, throwable: Throwable) {
                showConnectionError()
                markCatalogLoadFinished()
            }
        })
    }

    private fun loadServices() {
        ApiClient.service.getServices().enqueue(object : Callback<ApiResponse<List<ServiceResponse>>> {
            override fun onResponse(
                call: Call<ApiResponse<List<ServiceResponse>>>,
                response: Response<ApiResponse<List<ServiceResponse>>>
            ) {
                val body = response.body()
                if (response.isSuccessful && body?.success == true) {
                    services.clear()
                    services.addAll(body.data.orEmpty())
                    bindServices()
                } else {
                    showServerError(body?.error, "Error al cargar los servicios.")
                }
                markCatalogLoadFinished()
            }

            override fun onFailure(call: Call<ApiResponse<List<ServiceResponse>>>, throwable: Throwable) {
                showConnectionError()
                markCatalogLoadFinished()
            }
        })
    }

    private fun bindPets() {
        val labels = if (pets.isEmpty()) {
            listOf("No hay mascotas registradas")
        } else {
            pets.map { pet -> pet.name }
        }
        binding.spinnerMascota.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            labels
        )
    }

    private fun bindRooms() {
        val labels = if (rooms.isEmpty()) {
            listOf("No hay habitaciones disponibles")
        } else {
            rooms.map { room ->
                "${room.number} - ${room.name} (${room.roomType.toDisplayValue()})"
            }
        }
        binding.spinnerHabitacion.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            labels
        )
        updateLodgingType()
        updateTotal()
    }

    private fun bindServices() {
        binding.servicesContainer.removeAllViews()
        serviceChecks.clear()

        if (services.isEmpty()) {
            val emptyText = android.widget.TextView(this).apply {
                text = "No hay servicios adicionales disponibles."
                textSize = 13f
                setTextColor(getColor(R.color.text_light))
            }
            binding.servicesContainer.addView(emptyText)
            return
        }

        services.forEach { service ->
            val checkBox = CheckBox(this).apply {
                text = "${service.name} - ${formatCurrency(service.price)} por noche"
                textSize = 14f
                setTextColor(getColor(R.color.text_dark))
                setOnCheckedChangeListener { _, _ -> updateTotal() }
            }
            serviceChecks[service.id] = checkBox
            binding.servicesContainer.addView(checkBox)
        }
        updateLodgingType()
    }

    private fun submitReservation() {
        val selectedPet = pets.getOrNull(binding.spinnerMascota.selectedItemPosition)
        val selectedRoom = rooms.getOrNull(binding.spinnerHabitacion.selectedItemPosition)
        val checkIn = parseDateInput(binding.etFechaIngreso.text.toString())
        val checkOut = parseDateInput(binding.etFechaSalida.text.toString())

        if (selectedPet == null) {
            Toast.makeText(this, "Registra una mascota antes de reservar.", Toast.LENGTH_LONG).show()
            return
        }
        if (selectedRoom == null) {
            Toast.makeText(this, "Selecciona una habitación disponible.", Toast.LENGTH_LONG).show()
            return
        }
        if (checkIn == null) {
            binding.etFechaIngreso.error = "Usa YYYY-MM-DD o DD/MM/YYYY."
            return
        }
        if (checkOut == null) {
            binding.etFechaSalida.error = "Usa YYYY-MM-DD o DD/MM/YYYY."
            return
        }
        if (daysBetween(checkIn, checkOut) <= 0) {
            binding.etFechaSalida.error = "La salida debe ser después del ingreso."
            return
        }

        val lodgingType = selectedRoom.roomType
        val serviceIds = if (lodgingType == "special") {
            serviceChecks.filterValues { it.isChecked }.keys.toList()
        } else {
            emptyList()
        }
        val notes = binding.etNotas.text.toString().trim().ifBlank { null }
        val request = ReservationCreateRequest(
            petId = selectedPet.id,
            roomId = selectedRoom.id,
            checkInDate = outputDateFormat.format(checkIn),
            checkOutDate = outputDateFormat.format(checkOut),
            lodgingType = lodgingType,
            notes = notes,
            serviceIds = serviceIds
        )

        setSubmitting(true)
        ApiClient.service.createReservation(request)
            .enqueue(object : Callback<ApiResponse<ReservationResponse>> {
                override fun onResponse(
                    call: Call<ApiResponse<ReservationResponse>>,
                    response: Response<ApiResponse<ReservationResponse>>
                ) {
                    setSubmitting(false)
                    val body = response.body()
                    if (response.isSuccessful && body?.success == true) {
                        Toast.makeText(
                            this@CrearReservaActivity,
                            body.message ?: "Reserva creada exitosamente.",
                            Toast.LENGTH_LONG
                        ).show()
                        finish()
                    } else {
                        showServerError(body?.error, "Error al crear la reserva.")
                    }
                }

                override fun onFailure(
                    call: Call<ApiResponse<ReservationResponse>>,
                    throwable: Throwable
                ) {
                    setSubmitting(false)
                    showConnectionError()
                }
            })
    }

    private fun updateLodgingType() {
        val room = rooms.getOrNull(binding.spinnerHabitacion.selectedItemPosition)
        val isSpecial = room?.roomType == "special"
        binding.tvTipoHospedaje.text = when {
            room == null -> "Selecciona una habitación para ver el tipo de hospedaje."
            isSpecial -> "Hospedaje especial: puedes agregar servicios adicionales."
            else -> "Hospedaje estándar: servicios adicionales no disponibles."
        }

        serviceChecks.values.forEach { checkBox ->
            checkBox.isEnabled = isSpecial
            if (!isSpecial) {
                checkBox.isChecked = false
            }
        }
    }

    private fun updateTotal() {
        val room = rooms.getOrNull(binding.spinnerHabitacion.selectedItemPosition)
        val checkIn = parseDateInput(binding.etFechaIngreso.text.toString())
        val checkOut = parseDateInput(binding.etFechaSalida.text.toString())
        val nights = if (checkIn != null && checkOut != null) {
            daysBetween(checkIn, checkOut).coerceAtLeast(0)
        } else {
            0
        }
        val roomTotal = (room?.pricePerNight ?: 0.0) * nights
        val servicesTotal = if (room?.roomType == "special") {
            serviceChecks.mapNotNull { entry ->
                if (entry.value.isChecked) {
                    services.firstOrNull { service -> service.id == entry.key }?.price
                } else {
                    null
                }
            }.sum() * nights
        } else {
            0.0
        }
        binding.tvTotal.text = "Total estimado: ${formatCurrency(roomTotal + servicesTotal)}"
    }

    private fun markCatalogLoadFinished() {
        pendingCatalogLoads -= 1
        if (pendingCatalogLoads <= 0) {
            setLoading(false)
            if (pets.isEmpty()) {
                Toast.makeText(this, "Necesitas registrar una mascota antes de reservar.", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun setLoading(isLoading: Boolean) {
        binding.btnSave.isEnabled = !isLoading
        binding.btnVerificarDisponibilidad.isEnabled = !isLoading
        binding.btnBackToReservas.isEnabled = !isLoading
        binding.btnSave.text = if (isLoading) "Cargando..." else "Confirmar Reserva"
    }

    private fun setSubmitting(isSubmitting: Boolean) {
        binding.btnSave.isEnabled = !isSubmitting
        binding.btnVerificarDisponibilidad.isEnabled = !isSubmitting
        binding.btnBackToReservas.isEnabled = !isSubmitting
        binding.btnSave.text = if (isSubmitting) "Guardando..." else "Confirmar Reserva"
    }

    private fun parseDateInput(value: String): Date? {
        val trimmed = value.trim()
        if (trimmed.isBlank()) {
            return null
        }
        return inputDateFormats.firstNotNullOfOrNull { format ->
            try {
                format.parse(trimmed)
            } catch (exception: ParseException) {
                null
            }
        }
    }

    private fun daysBetween(start: Date, end: Date): Int {
        val diff = end.time - start.time
        return TimeUnit.MILLISECONDS.toDays(diff).toInt()
    }

    private fun datePlusDays(date: Date, days: Int): Date =
        Calendar.getInstance().apply {
            time = date
            add(Calendar.DAY_OF_YEAR, days)
        }.time

    private fun Date.atStartOfDay(): Date =
        Calendar.getInstance().apply {
            time = this@atStartOfDay
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }.time

    private fun formatCurrency(value: Double): String =
        "CRC ${String.format(Locale.US, "%,.2f", value)}"

    private fun showServerError(error: String?, fallback: String) {
        Toast.makeText(this, error ?: fallback, Toast.LENGTH_LONG).show()
    }

    private fun showConnectionError() {
        Toast.makeText(this, "Error al conectar con el servidor.", Toast.LENGTH_LONG).show()
    }

    private fun String.toDisplayValue(): String = when (this) {
        "standard" -> "Estándar"
        "special" -> "Especial"
        else -> replaceFirstChar { character ->
            if (character.isLowerCase()) character.titlecase() else character.toString()
        }
    }

    companion object {
        private val outputDateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.US).apply {
            isLenient = false
        }
        private val inputDateFormats = listOf(
            SimpleDateFormat("yyyy-MM-dd", Locale.US).apply { isLenient = false },
            SimpleDateFormat("dd/MM/yyyy", Locale.US).apply { isLenient = false },
        )
    }
}
