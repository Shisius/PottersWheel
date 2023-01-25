#ifndef _TIMER1FWM_H_
#define _TIMER1FWM_H_

// Uses pin 9

#define F_CPU 16000000

#define TMR_PRECS_MASK 0x07
#define TMR_PRECS_NUMBER 6

static unit8_t TIMER1_PRESCALERS[TMR_PRECS_NUMBER] = {0, 1, 8, 64, 256, 1024};

inline void fwm_init()
{
	// Set Pin 9 as OUT
	DDRB |= (1 << PB1); 

	// Clear timer control regs
	TCCR1A = 0;
	TCCR1B = 0;

	// Set non-inverting mode
	TCCR1A |= (1 << COM1A1);

	// Set fast PWM Mode, TOP = ICR1
	TCCR1A |= (1 << WGM11);
	TCCR1B |= (1 << WGM12);
	TCCR1B |= (1 << WGM13);

	sei();
}

inline void fwm_set_precs(uint8_t presc)
{
	TCCR1B = (TCCR1B & (~TMR_PRECS_MASK)) | presc; // SET CS to 0
}

inline void fwm_stop()
{
	fwm_set_precs(0); 
}

inline void fwm_set_duty(float duty)
{
	float duty_reg = float(ICR1A) * duty / 100.0;
	OCR1A = (uit16_t)round(duty_reg);
}

inline void fwm_set_freq(float freq)
{
	uint8_t precs_ind = 1;
	float freq_reg;
	while (precs_ind < TMR_PRECS_NUMBER) {
		freq_reg = (F_CPU / (TIMER1_PRESCALERS[precs_ind] * freq)) - 1;
		if (freq_reg <= 65535 && freq_reg >= 1) {
			fwm_set_precs(precs_ind);
			ICR1 = (uint16_t)round(freq_reg);
			return;
		}
		precs_ind++;
	}
}

#endif //_TIMER1FWM_H_

