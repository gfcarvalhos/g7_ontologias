from owlready2 import *

# Criar um novo arquivo de ontologia
onto = get_ontology("http://example.org/full_health.owl")

with onto:
    ### **1. Definir Classes**
    class Paciente(Thing): pass
    class Sintoma(Thing): pass
    class Doenca(Thing): pass
    class Exame(Thing): pass
    class Tratamento(Thing): pass

    ### **2. Subclasses**
    # Sintomas
    class SintomaRespiratorio(Sintoma): pass
    class SintomaCardiaco(Sintoma): pass
    class SintomaGastrointestinal(Sintoma): pass

    # Doenças
    class DoencaInfecciosa(Doenca): pass
    class DoencaCronica(Doenca): pass
    class DoencaGastrointestinal(Doenca): pass
    class DoencaRespiratoria(Doenca): pass

    # Exames
    class ExameImagem(Exame): pass
    class ExameLaboratorial(Exame): pass
    class ExameFuncional(Exame): pass

    # Tratamentos
    class TratamentoMedicamentoso(Tratamento): pass
    class TratamentoNaoMedicamentoso(Tratamento): pass

    ### **3. Propriedades**
    class apresenta(ObjectProperty):
        domain = [Paciente]
        range = [Sintoma]

    class diagnosticado_com(ObjectProperty):
        domain = [Paciente]
        range = [Doenca]
        is_functional = True  # Um paciente só pode ser diagnosticado com uma doença por vez

    class requer_exame(ObjectProperty):
        domain = [Sintoma]
        range = [Exame]

    class confirmada_por(ObjectProperty):
        domain = [Doenca]
        range = [Exame]
        is_transitive = True  # Propriedade transitiva

    class tratada_com(ObjectProperty):
        domain = [Doenca]
        range = [Tratamento]

    ### **4. Adicionar Axiomas**
    Paciente.equivalent_to = [
        Thing & apresenta.some(Sintoma)  # Todo paciente deve apresentar pelo menos um sintoma
    ]
    Sintoma.equivalent_to = [
        Thing & requer_exame.some(Exame)  # Todo sintoma deve estar relacionado a pelo menos um exame
    ]
    SintomaRespiratorio.equivalent_to = [
        Sintoma & requer_exame.some(ExameImagem)  # Sintomas respiratórios requerem exames de imagem
    ]
    SintomaCardiaco.equivalent_to = [
        Sintoma & requer_exame.some(ExameFuncional | ExameLaboratorial)  # Sintomas cardíacos requerem exames funcionais ou laboratoriais
    ]
    SintomaGastrointestinal.equivalent_to = [
        Sintoma & requer_exame.some(ExameImagem | ExameLaboratorial)  # Sintomas gastrointestinais requerem exames laboratoriais ou de imagem
    ]
    Doenca.equivalent_to = [
        Thing & confirmada_por.some(Exame)  # Toda doença deve ser confirmada por pelo menos um exame
    ]
    DoencaInfecciosa.equivalent_to = [
        Doenca & confirmada_por.some(ExameLaboratorial)  # Doenças infecciosas requerem exames laboratoriais
    ]
    DoencaCronica.equivalent_to = [
        Doenca & confirmada_por.some(ExameLaboratorial | ExameFuncional)  # Doenças crônicas requerem exames laboratoriais ou funcionais
    ]
    DoencaGastrointestinal.equivalent_to = [
        Doenca & confirmada_por.some(ExameImagem | ExameLaboratorial)  # Doenças gastrointestinais requerem exames laboratoriais ou de imagem
    ]
    DoencaRespiratoria.equivalent_to = [
        Doenca & confirmada_por.some(ExameImagem)  # Doenças respiratórias requerem exames de imagem
    ]
    Tratamento.equivalent_to = [
        Thing & tratada_com.some(Doenca)  # Todo tratamento deve estar relacionado a pelo menos uma doença
    ]
    TratamentoMedicamentoso.equivalent_to = [
        Tratamento & tratada_com.some(Doenca)  # Tratamentos medicamentosos estão relacionados a doenças confirmadas
    ]
    TratamentoNaoMedicamentoso.equivalent_to = [
        Tratamento & tratada_com.some(DoencaCronica | DoencaRespiratoria)  # Tratamentos não medicamentosos tratam doenças crônicas ou respiratórias
    ]

    ### **5. Instâncias**
    # Sintomas
    febre = SintomaRespiratorio("Febre")
    tosse = SintomaRespiratorio("Tosse")
    dor_no_peito = SintomaCardiaco("Dor no peito")
    nauseas = SintomaGastrointestinal("Náuseas")
    diarreia = SintomaGastrointestinal("Diarreia")
    falta_ar = SintomaRespiratorio("Falta de ar")

    # Exames
    raio_x = ExameImagem("Raio-X")
    tomografia = ExameImagem("Tomografia Computadorizada")
    hemograma = ExameLaboratorial("Hemograma Completo")
    gasometria = ExameLaboratorial("Gasometria")
    teste_esforco = ExameFuncional("Teste de Esforço")
    endoscopia = ExameImagem("Endoscopia Digestiva")

    # Doenças
    covid19 = DoencaInfecciosa("COVID-19")
    pneumonia = DoencaRespiratoria("Pneumonia")
    hipertensao = DoencaCronica("Hipertensão")
    gastrite = DoencaGastrointestinal("Gastrite")
    insuficiencia_respiratoria = DoencaRespiratoria("Insuficiência Respiratória")

    # Tratamentos
    isolamento = TratamentoNaoMedicamentoso("Isolamento")
    antiviral = TratamentoMedicamentoso("Antiviral")
    dieta_baixa_acidez = TratamentoNaoMedicamentoso("Dieta Baixa em Acidez")
    antibiotico = TratamentoMedicamentoso("Antibiótico")
    suplemento_oxigenio = TratamentoNaoMedicamentoso("Suplemento de Oxigênio")
    anti_hipertensivo = TratamentoMedicamentoso("Medicamento Anti-hipertensivo")

    # Pacientes
    paciente1 = Paciente("Joao")
    paciente2 = Paciente("Maria")

    ### **6. Relacionar Instâncias**
    febre.requer_exame = [hemograma, tomografia]
    tosse.requer_exame = [raio_x]
    dor_no_peito.requer_exame = [teste_esforco]
    nauseas.requer_exame = [endoscopia]
    diarreia.requer_exame = [endoscopia, hemograma]
    falta_ar.requer_exame = [gasometria, tomografia]

    covid19.confirmada_por = [raio_x, hemograma]
    pneumonia.confirmada_por = [raio_x, tomografia]
    hipertensao.confirmada_por = [teste_esforco, hemograma]
    gastrite.confirmada_por = [endoscopia, hemograma]
    insuficiencia_respiratoria.confirmada_por = [gasometria, tomografia]

    covid19.tratada_com = [isolamento, antiviral]
    pneumonia.tratada_com = [antibiotico, suplemento_oxigenio]
    hipertensao.tratada_com = [anti_hipertensivo]
    gastrite.tratada_com = [dieta_baixa_acidez]
    insuficiencia_respiratoria.tratada_com = [suplemento_oxigenio]

    paciente1.apresenta = [febre, tosse, falta_ar]
    paciente2.apresenta = [nauseas, diarreia, dor_no_peito]

    paciente1.diagnosticado_com = [covid19]
    paciente2.diagnosticado_com = [gastrite, hipertensao]

### **7. Salvar a Ontologia**
onto.save("full_health.owl")
print("Ontologia criada e salva no arquivo 'full_health_with_instances.owl'")
