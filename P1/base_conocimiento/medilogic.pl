% ==============================================================================
% HECHOS: SÍNTOMAS
% ==============================================================================
% sintoma(ID, Nombre, Descripcion, Sistema)
sintoma(s1, 'Fiebre', 'Temperatura corporal elevada', 'general').
sintoma(s2, 'Tos', 'Tos seca o con flema', 'respiratorio').
sintoma(s3, 'Dolor de cabeza', 'Cefalea o migraña', 'neurologico').
sintoma(s4, 'Dolor de garganta', 'Irritación o dolor al tragar', 'respiratorio').
sintoma(s5, 'Fatiga', 'Cansancio extremo', 'general').
sintoma(s6, 'Náuseas', 'Sensación de vómito', 'digestivo').
sintoma(s7, 'Vómito', 'Expulsión del contenido estomacal', 'digestivo').
sintoma(s8, 'Diarrea', 'Evacuaciones líquidas frecuentes', 'digestivo').
sintoma(s9, 'Dolor abdominal', 'Dolor en el área del abdomen', 'digestivo').
sintoma(s10, 'Congestión nasal', 'Nariz tapada', 'respiratorio').
sintoma(s11, 'Dolor muscular', 'Dolor en músculos', 'musculoesqueletico').
sintoma(s12, 'Sudoración excesiva', 'Transpiración abundante', 'general').
sintoma(s13, 'Mareo', 'Sensación de inestabilidad', 'neurologico').
sintoma(s14, 'Dolor de pecho', 'Molestia torácica', 'cardiovascular').
sintoma(s15, 'Dificultad para respirar', 'Disnea', 'respiratorio').

% ==============================================================================
% HECHOS: ENFERMEDADES
% ==============================================================================
% enfermedad(ID, Nombre, Descripcion, Sistema, Tipo, Gravedad)
% Gravedad: leve, moderada, grave
enfermedad(e1, 'Gripe', 'Infección viral del sistema respiratorio', 'respiratorio', 'viral', 'moderada').
enfermedad(e2, 'Resfriado común', 'Infección viral leve de vías respiratorias', 'respiratorio', 'viral', 'leve').
enfermedad(e3, 'Gastroenteritis', 'Inflamación del tracto gastrointestinal', 'digestivo', 'viral', 'moderada').
enfermedad(e4, 'Migraña', 'Dolor de cabeza intenso', 'neurologico', 'cronico', 'moderada').
enfermedad(e5, 'Bronquitis', 'Inflamación de los bronquios', 'respiratorio', 'viral', 'moderada').
enfermedad(e6, 'Neumonía', 'Infección pulmonar', 'respiratorio', 'bacterial', 'grave').
enfermedad(e7, 'Faringitis', 'Inflamación de la faringe', 'respiratorio', 'viral', 'leve').
enfermedad(e8, 'COVID-19', 'Enfermedad por coronavirus', 'respiratorio', 'viral', 'grave').

% ==============================================================================
% RELACIONES: ENFERMEDAD - SÍNTOMAS
% ==============================================================================
% presenta_sintoma(EnfermedadID, SintomaID, Peso)
% Peso: importancia del síntoma (1-10)

% Gripe (e1)
presenta_sintoma(e1, s1, 9).  % Fiebre
presenta_sintoma(e1, s2, 7).  % Tos
presenta_sintoma(e1, s3, 6).  % Dolor de cabeza
presenta_sintoma(e1, s5, 8).  % Fatiga
presenta_sintoma(e1, s11, 7). % Dolor muscular
presenta_sintoma(e1, s10, 6). % Congestión nasal

% Resfriado común (e2)
presenta_sintoma(e2, s10, 9). % Congestión nasal
presenta_sintoma(e2, s2, 6).  % Tos
presenta_sintoma(e2, s4, 7).  % Dolor de garganta
presenta_sintoma(e2, s3, 4).  % Dolor de cabeza
presenta_sintoma(e2, s5, 5).  % Fatiga

% Gastroenteritis (e3)
presenta_sintoma(e3, s6, 8).  % Náuseas
presenta_sintoma(e3, s7, 7).  % Vómito
presenta_sintoma(e3, s8, 9).  % Diarrea
presenta_sintoma(e3, s9, 8).  % Dolor abdominal
presenta_sintoma(e3, s1, 5).  % Fiebre

% Migraña (e4)
presenta_sintoma(e4, s3, 10). % Dolor de cabeza intenso
presenta_sintoma(e4, s6, 6).  % Náuseas
presenta_sintoma(e4, s13, 5). % Mareo

% Bronquitis (e5)
presenta_sintoma(e5, s2, 10). % Tos persistente
presenta_sintoma(e5, s14, 6). % Dolor de pecho
presenta_sintoma(e5, s5, 7).  % Fatiga
presenta_sintoma(e5, s1, 5).  % Fiebre

% Neumonía (e6)
presenta_sintoma(e6, s1, 9).  % Fiebre alta
presenta_sintoma(e6, s2, 9).  % Tos
presenta_sintoma(e6, s15, 10).% Dificultad para respirar
presenta_sintoma(e6, s14, 8). % Dolor de pecho
presenta_sintoma(e6, s5, 9).  % Fatiga

% Faringitis (e7)
presenta_sintoma(e7, s4, 10). % Dolor de garganta
presenta_sintoma(e7, s1, 6).  % Fiebre
presenta_sintoma(e7, s3, 4).  % Dolor de cabeza

% COVID-19 (e8)
presenta_sintoma(e8, s1, 8).  % Fiebre
presenta_sintoma(e8, s2, 8).  % Tos seca
presenta_sintoma(e8, s5, 9).  % Fatiga
presenta_sintoma(e8, s15, 8). % Dificultad para respirar
presenta_sintoma(e8, s11, 7). % Dolor muscular
presenta_sintoma(e8, s3, 6).

% Neumonía Atípica (e9)
presenta_sintoma(e9, s1, 7).
presenta_sintoma(e9, s2, 7).
presenta_sintoma(e9, s15, 7).
presenta_sintoma(e9, s5, 7).

% Bronquitis Aguda (e12)
presenta_sintoma(e12, s1, 7).
presenta_sintoma(e12, s2, 7).
presenta_sintoma(e12, s5, 7).

% Síndrome de Intestino Irritable (e13)
presenta_sintoma(e13, s6, 7).
presenta_sintoma(e13, s9, 7).

% Gastritis Aguda (e10)
presenta_sintoma(e10, s6, 7).
presenta_sintoma(e10, s9, 7).

% Arritmia Cardíaca (e11)
presenta_sintoma(e11, s11, 7).
presenta_sintoma(e11, s14, 7).








  % Dolor de cabeza

% ==============================================================================
% HECHOS: MEDICAMENTOS
% ==============================================================================
% medicamento(ID, Nombre, Principio, Tipo, Descripcion)
medicamento(m1, 'Paracetamol', 'Paracetamol', 'analgesico', 'Reduce fiebre y dolor').
medicamento(m2, 'Ibuprofeno', 'Ibuprofeno', 'antiinflamatorio', 'Reduce inflamación y dolor').
medicamento(m3, 'Amoxicilina', 'Amoxicilina', 'antibiotico', 'Antibiótico de amplio espectro').
medicamento(m4, 'Omeprazol', 'Omeprazol', 'antiácido', 'Protector gástrico').
medicamento(m5, 'Loratadina', 'Loratadina', 'antihistamínico', 'Para alergias').
medicamento(m6, 'Dextrometorfano', 'Dextrometorfano', 'antitusivo', 'Supresor de tos').
medicamento(m7, 'Suero oral', 'Sales de rehidratación', 'hidratante', 'Rehidratación').
medicamento(m8, 'Azitromicina', 'Azitromicina', 'antibiotico', 'Antibiótico macrólido').

% ==============================================================================
% RELACIONES: ENFERMEDAD - TRATAMIENTO
% ==============================================================================
% trata_enfermedad(MedicamentoID, EnfermedadID, Efectividad)
% Efectividad: 1-10

% Gripe
trata_enfermedad(m1, e1, 8).  % Paracetamol
trata_enfermedad(m2, e1, 7).  % Ibuprofeno

% Resfriado común
trata_enfermedad(m1, e2, 7).  % Paracetamol
trata_enfermedad(m5, e2, 6).  % Loratadina

% Gastroenteritis
trata_enfermedad(m7, e3, 9).  % Suero oral
trata_enfermedad(m4, e3, 6).  % Omeprazol

% Migraña
trata_enfermedad(m1, e4, 7).  % Paracetamol
trata_enfermedad(m2, e4, 8).  % Ibuprofeno

% Bronquitis
trata_enfermedad(m6, e5, 7).  % Dextrometorfano
trata_enfermedad(m3, e5, 8).  % Amoxicilina

% Neumonía
trata_enfermedad(m3, e6, 9).  % Amoxicilina
trata_enfermedad(m8, e6, 9).  % Azitromicina

% Faringitis
trata_enfermedad(m1, e7, 7).  % Paracetamol
trata_enfermedad(m3, e7, 8).  % Amoxicilina

% COVID-19
trata_enfermedad(m1, e8, 7).
enfermedad(e9, 'Neumonía Atípica', 'Infección pulmonar causada por agentes atípicos como Mycoplasma pneumoniae', 'respiratorio', 'bacterial', 'grave').
enfermedad(e12, 'Bronquitis Aguda', 'Inflamación de los bronquios que transportan aire a los pulmones', 'respiratorio', 'viral', 'moderada').
enfermedad(e13, 'Síndrome de Intestino Irritable', 'Trastorno funcional del aparato digestivo', 'digestivo', 'cronico', 'leve').
enfermedad(e10, 'Gastritis Aguda', 'Inflamación repentina del revestimiento del estómago', 'digestivo', 'general', 'moderada').
enfermedad(e11, 'Arritmia Cardíaca', 'Alteración del ritmo cardíaco normal', 'cardiovascular', 'cronico', 'grave').








  % Paracetamol (sintomático)

% ==============================================================================
% HECHOS: ENFERMEDADES CRÓNICAS
% ==============================================================================
% enfermedad_cronica(ID, Nombre, Sistema)
enfermedad_cronica(ec1, 'Diabetes', 'endocrino').
enfermedad_cronica(ec2, 'Hipertensión', 'cardiovascular').
enfermedad_cronica(ec3, 'Asma', 'respiratorio').
enfermedad_cronica(ec4, 'Enfermedad renal crónica', 'renal').
enfermedad_cronica(ec5, 'Enfermedad hepática', 'hepatico').

% ==============================================================================
% CONTRAINDICACIONES
% ==============================================================================
% contraindicado(MedicamentoID, EnfermedadCronicaID, Razon)
contraindicado(m2, ec1, 'Ibuprofeno puede afectar niveles de glucosa').
contraindicado(m2, ec2, 'Ibuprofeno aumenta presión arterial').
contraindicado(m2, ec4, 'Ibuprofeno afecta función renal').
contraindicado(m3, ec5, 'Amoxicilina metabolizada en hígado').

% ==============================================================================
% REGLAS DE INFERENCIA
% ==============================================================================

% Calcular afinidad entre síntomas del paciente y enfermedad
% calcular_afinidad(+ListaSintomas, +EnfermedadID, -Afinidad)
calcular_afinidad(ListaSintomas, EnfermedadID, Afinidad) :-
    enfermedad(EnfermedadID, _, _, _, _, _),
    findall(PesoAjustado, (
        member(sintoma(SID, Severidad), ListaSintomas),
        presenta_sintoma(EnfermedadID, SID, Peso),
        ajustar_peso(Peso, Severidad, PesoAjustado)
    ), PesosEncontrados),
    findall(PesoTotal, presenta_sintoma(EnfermedadID, _, PesoTotal), TodosPesos),
    sum_list(PesosEncontrados, SumaEncontrados),
    sum_list(TodosPesos, SumaTotal),
    (SumaTotal > 0 -> Afinidad is (SumaEncontrados / SumaTotal) * 100 ; Afinidad is 0).

% Ajustar peso según severidad del síntoma
ajustar_peso(Peso, leve, PesoAjustado) :- PesoAjustado is Peso * 0.7.
ajustar_peso(Peso, moderado, PesoAjustado) :- PesoAjustado is Peso * 1.0.
ajustar_peso(Peso, severo, PesoAjustado) :- PesoAjustado is Peso * 1.3.

% Determinar nivel de urgencia
nivel_urgencia(Afinidad, Gravedad, Urgencia) :-
    (Afinidad >= 70, Gravedad = grave -> Urgencia = 'Consulta médica inmediata sugerida'
    ; Afinidad >= 60, Gravedad = moderada -> Urgencia = 'Consulta médica recomendada'
    ; Afinidad >= 50 -> Urgencia = 'Observación recomendada'
    ; Urgencia = 'Posible automanejo con precaución').

% Verificar si un medicamento es seguro para el paciente
medicamento_seguro(MedicamentoID, Alergias, EnfermedadesCronicas) :-
    medicamento(MedicamentoID, Nombre, _, _, _),
    \+ member(Nombre, Alergias),
    \+ (member(ECID, EnfermedadesCronicas), contraindicado(MedicamentoID, ECID, _)).

% Obtener medicamentos seguros para una enfermedad
obtener_medicamentos_seguros(EnfermedadID, Alergias, EnfermedadesCronicas, Medicamentos) :-
    findall(
        medicamento(ID, Nombre, Tipo, Efectividad),
        (
            trata_enfermedad(ID, EnfermedadID, Efectividad),
            medicamento_seguro(ID, Alergias, EnfermedadesCronicas),
            medicamento(ID, Nombre, _, Tipo, _)
        ),
        Medicamentos
    ).

% Diagnóstico principal
diagnosticar(ListaSintomas, Alergias, EnfermedadesCronicas, Diagnosticos) :-
    findall(
        diagnostico(EnfID, Nombre, Afinidad, Gravedad, Urgencia, Medicamentos),
        (
            calcular_afinidad(ListaSintomas, EnfID, Afinidad),
            Afinidad > 30,  % Umbral mínimo
            enfermedad(EnfID, Nombre, _, _, _, Gravedad),
            nivel_urgencia(Afinidad, Gravedad, Urgencia),
            obtener_medicamentos_seguros(EnfID, Alergias, EnfermedadesCronicas, Medicamentos)
        ),
        DiagnosticosTemp
    ),
    sort(3, @>=, DiagnosticosTemp, Diagnosticos).  % Ordenar por afinidad descendente

% ==============================================================================
% FIN DEL ARCHIVO
% ==============================================================================
