% ==============================================================================
% ARCHIVO DE PRUEBA MINIMO PARA CARGA DE BASE PROLOG
% ==============================================================================

:- dynamic enfermedad/6.
:- dynamic sintoma/4.
:- dynamic medicamento/5.
:- dynamic presenta_sintoma/3.
:- dynamic trata_enfermedad/3.
:- dynamic contraindicacion/3.

% ==================== HECHOS: SINTOMAS ====================
sintoma(s1, 'Fiebre', 'Temperatura alta', 'general').
sintoma(s2, 'Tos', 'Tos persistente', 'respiratorio').

% ==================== HECHOS: ENFERMEDADES ====================
enfermedad(e1, 'Gripe Leve', 'Infeccion viral respiratoria leve', 'respiratorio', 'viral', 'leve').

% ==================== HECHOS: MEDICAMENTOS ====================
medicamento(m1, 'Paracetamol', 'Paracetamol', 'analgesico', 'Alivia fiebre y dolor').

% ==================== RELACIONES ====================
presenta_sintoma(e1, s1, 9).
presenta_sintoma(e1, s2, 7).
trata_enfermedad(m1, e1, 8).
contraindicacion(m1, e1, 'Evitar dosis altas en pacientes con dano hepatico').
