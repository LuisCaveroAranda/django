from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from django.shortcuts import get_object_or_404,render
import pandas as pd
from sklearn import svm
import datetime
from .models import Examen

hora_actual = datetime.datetime.now()

print(hora_actual)

# Create your views here.

nombres=""
edad=""
horaInicioTest=""
horaFinTest=""
horaInicioPro=""
horaFinPro=""

#Muestra el frame de Inicio
def index(request):
    nombres=""
    edad=""
    return render(request,"index.html")

def iniciarProceso(request):
    if request.method=="POST":
        global nombres,edad,horaInicioTest
        nombres=request.POST["nombres"]
        edad=request.POST["edad"]
        horaInicioTest = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context= {"nombres":nombres,"edad":edad,}
        return render(request,'proceso.html',context)
    else:
        return render(request,"index.html")
    
#Muestra el frame realizar Emcuesta
def resultados(request):
    if request.method=="POST":
        global horaFinTest,horaInicioPro,horaFinPro
        horaFinTest= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        horaInicioPro= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        interes= np.array([[int(request.POST["r98"]),int(request.POST["r9"]),int(request.POST["r21"]),int(request.POST["r33"]),int(request.POST["r75"]),int(request.POST["r84"]),int(request.POST["r77"])],[int(request.POST["r12"]),int(request.POST["r34"]),int(request.POST["r45"]),int(request.POST["r92"]),int(request.POST["r6"]),int(request.POST["r31"]),int(request.POST["r42"])],[int(request.POST["r64"]),int(request.POST["r80"]),int(request.POST["r96"]),int(request.POST["r70"]),int(request.POST["r19"]),int(request.POST["r48"]),int(request.POST["r88"])],[int(request.POST["r53"]),int(request.POST["r25"]),int(request.POST["r57"]),int(request.POST["r8"]),int(request.POST["r38"]),int(request.POST["r73"]),int(request.POST["r17"])],[int(request.POST["r85"]),int(request.POST["r95"]),int(request.POST["r28"]),int(request.POST["r87"]),int(request.POST["r60"]),int(request.POST["r5"]),int(request.POST["r93"])],[int(request.POST["r1"]),int(request.POST["r67"]),int(request.POST["r11"]),int(request.POST["r62"]),int(request.POST["r27"]),int(request.POST["r65"]),int(request.POST["r32"])],[int(request.POST["r78"]),int(request.POST["r41"]),int(request.POST["r50"]),int(request.POST["r23"]),int(request.POST["r83"]),int(request.POST["r14"]),int(request.POST["r68"])],[int(request.POST["r20"]),int(request.POST["r74"]),int(request.POST["r3"]),int(request.POST["r44"]),int(request.POST["r54"]),int(request.POST["r37"]),int(request.POST["r49"])],[int(request.POST["r71"]),int(request.POST["r56"]),int(request.POST["r81"]),int(request.POST["r16"]),int(request.POST["r47"]),int(request.POST["r58"]),int(request.POST["r35"])],[int(request.POST["r91"]),int(request.POST["r89"]),int(request.POST["r36"]),int(request.POST["r52"]),int(request.POST["r97"]),int(request.POST["r24"]),int(request.POST["r61"])]])
        
        aptitudes=np.array([[int(request.POST["r15"]),int(request.POST["r63"]),int(request.POST["r22"]),int(request.POST["r69"]),int(request.POST["r26"]),int(request.POST["r13"]),int(request.POST["r94"])],[int(request.POST["r51"]),int(request.POST["r30"]),int(request.POST["r39"]),int(request.POST["r40"]),int(request.POST["r59"]),int(request.POST["r66"]),int(request.POST["r7"])],[int(request.POST["r2"]),int(request.POST["r72"]),int(request.POST["r76"]),int(request.POST["r28"]),int(request.POST["r90"]),int(request.POST["r18"]),int(request.POST["r79"])],[int(request.POST["r46"]),int(request.POST["r86"]),int(request.POST["r82"]),int(request.POST["r4"]),int(request.POST["r10"]),int(request.POST["r43"]),int(request.POST["r55"])]])
        sumaInteres=interes.sum(axis=0)
        sumaAptitudes=aptitudes.sum(axis=0)
        modelo=entrenamientoModelo()
        modeloResultado=int(prediccion(modelo,sumaInteres,sumaAptitudes))
        
        horaFinPro= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        examen=Examen()
        examen.nombre=nombres
        examen.edad=edad
        examen.horaInicioTest=horaInicioTest
        examen.horaFinTest=horaFinTest
        examen.horaInicioPro=horaInicioPro
        examen.horaFinPro=horaFinPro
       
        mejoresCarrerass=mejoresCarreras(modeloResultado)
        professiones=()
        lista = list(professiones)
        for carrera in mejoresCarrerass:
            nombre,descripcion,direccionFoto=devolverPrefession(carrera)
            carreratop={'nombre': nombre,
                                 'descripcion':descripcion,
                                 'foto': direccionFoto}
            lista.append(carreratop)
        nombre,descripcion,direccionFoto=devolverPrefession(modeloResultado)    
        context= {"nombres":nombres,"nombre":nombre,"descripcion":descripcion,"direccionFoto":direccionFoto,"professiones":lista}
        return render(request,'resultados.html',context)
    else:
        return render(request,"index.html")

            
def handler404(request,exception):
    return render(request,"not_found.html")
     

def devolverPrefession(idResultado):
    nombre=""
    descripcion=""
    direccionFoto=""
    professiones = ({
      'id': 1,
      'nombre': "Administracion de Empresas",
      'descripcion':'La administración de empresas es una carrera dinámica que se centra en la gestión eficiente de organizaciones para alcanzar sus objetivos. Abarca diversas áreas, desde la planificación estratégica hasta la gestión de recursos humanos y operaciones. En esencia, los administradores de empresas son los arquitectos del éxito de una organización. Planifican, organizan, dirigen y controlan los recursos para optimizar su funcionamiento y alcanzar metas establecidas. Es una carrera con alta demanda en el mercado laboral actual, ofreciendo oportunidades en diversos sectores y niveles jerárquicos..',
      'foto': "../static/ADMINISTRACION_DE_EMPRESAS.jpg",
    },{
      'id': 2,
      'nombre': "ingenieria Industrial",
      'descripcion':'La ingeniería industrial es una carrera apasionante que se enfoca en el diseño, análisis, mejora e implementación de sistemas integrados de producción, servicios y procesos. Su objetivo es optimizar el uso de recursos, la eficiencia operativa y la calidad en diversos ámbitos, desde empresas manufactureras hasta organizaciones de servicios.Los ingenieros industriales son como los detectives del mundo empresarial. Utilizan su conocimiento en matemáticas, física, informática y ciencias sociales para identificar problemas, analizar datos, desarrollar soluciones innovadoras y optimizar procesos. Su trabajo es crucial para que las organizaciones funcionen de manera eficiente, productiva y competitiva.Si te apasionan los desafíos, la resolución de problemas y la búsqueda de la mejora continua, la ingeniería industrial puede ser la carrera perfecta para ti. Te permitirá desarrollar habilidades altamente valoradas en el mercado laboral y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos sectores..',
      'foto': "../static/INGENIERIA_INDUSTRIAL.jpg",
    },{
      'id': 3,
      'nombre': "Contabilidad",
      'descripcion':'La contabilidad es una carrera fundamental para el funcionamiento de cualquier organización. Se encarga de registrar, clasificar, analizar e interpretar las transacciones financieras de una empresa o entidad. Es como el sistema nervioso de una organización, proporcionando información vital para la toma de decisiones estratégicas.Los contadores son los guardianes de las finanzas. Registran meticulosamente cada entrada y salida de dinero, generan informes financieros detallados y analizan el estado financiero de la organización. Su trabajo es esencial para garantizar la transparencia, la solvencia y el cumplimiento de las obligaciones fiscales y legales.Si te gustan los números, la organización y la precisión, la contabilidad puede ser una carrera gratificante para ti. Te permitirá desarrollar habilidades altamente demandadas en el mercado laboral y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos sectores, incluyendo empresas privadas, instituciones públicas, despachos contables y auditorías.',
      'foto': "../static/CONTABILIDAD.jpg",
    },{
      'id': 4,
      'nombre': "Gastronomia",
      'descripcion':'La gastronomía es una carrera apasionante que combina el arte culinario con la ciencia de los alimentos. Se trata de un campo de estudio dinámico y creativo que explora la relación entre la comida, la cultura y la sociedad. Los profesionales de la gastronomía son como artistas culinarios. Dominan las técnicas de cocina, exploran los sabores del mundo, crean recetas innovadoras y comparten su pasión por la comida con los demás. Si te apasiona la cocina, te encanta experimentar con nuevos sabores y te interesa conocer la historia y cultura detrás de la comida, la gastronomía puede ser la carrera perfecta para ti. Te permitirá desarrollar habilidades culinarias, conocimientos nutricionales y una visión creativa que te abrirán las puertas a un mundo de oportunidades en el sector culinario.',
      'foto': "../static/GASTRONOMIA.jpg",
    },{
      'id': 5,
      'nombre': "Psicologia",
      'descripcion':'La psicología es una disciplina fascinante que se dedica al estudio de la mente y el comportamiento humano. Su objetivo es comprender los procesos mentales, las emociones, la personalidad y las relaciones interpersonales que nos definen como individuos y como sociedad. Los psicólogos son como exploradores del mundo interior. Utilizan su conocimiento en biología, neurociencia, ciencias sociales y estadística para investigar, evaluar, diagnosticar y tratar problemas mentales, emocionales y conductuales. Su trabajo es fundamental para promover el bienestar individual, familiar y social, y para mejorar la calidad de vida de las personas. Si te interesa comprender la complejidad de la mente humana, ayudar a las personas a superar sus dificultades y contribuir al bienestar de la sociedad, la psicología puede ser la carrera ideal para ti. Te permitirá desarrollar habilidades valiosas en comunicación, empatía, análisis y resolución de problemas, y te abrirá las puertas a un mundo de oportunidades profesionales en diversos ámbitos, como la salud mental, la educación, la investigación y las organizaciones.',
      'foto': "../static/PSICOLOGIA.jpg",
    },{
      'id': 6,
      'nombre': "Derecho",
      'descripcion':'El derecho es una carrera apasionante y desafiante que se centra en la búsqueda de la justicia, el orden social y la protección de los derechos individuales. Abarca un amplio espectro de áreas, desde el derecho civil y penal hasta el derecho constitucional y administrativo. Los abogados, como se les conoce a los profesionales del derecho, son los defensores de la ley y los guardianes de los derechos. Analizan leyes, asesoran a clientes, representan a individuos y organizaciones en procesos legales y trabajan para garantizar que se haga justicia en cada caso. Si te apasiona la justicia, la defensa de los derechos y la búsqueda de soluciones justas a problemas complejos, el derecho puede ser la carrera perfecta para ti. Te permitirá desarrollar habilidades analíticas, de investigación, argumentativas y de comunicación excepcionales, y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos ámbitos, tanto en el sector público como en el privado.',
      'foto': "../static/DERECHO.jpg",
    },{
      'id': 7,
      'nombre': "Educacion",
      'descripcion':'La educación es una carrera noble y transformadora que se centra en la formación integral de las personas, preparando a las nuevas generaciones para enfrentar los retos del mundo actual. Abarca diversos aspectos, desde la pedagogía y la didáctica hasta la psicología del desarrollo y la evaluación del aprendizaje. En esencia, los educadores son los arquitectos del conocimiento y el cambio. Son responsables de guiar a los estudiantes en su proceso de aprendizaje, fomentando el pensamiento crítico, la creatividad, la colaboración y el desarrollo de habilidades esenciales para la vida. Es una carrera con un impacto profundo en la sociedad, pues contribuye al desarrollo individual y colectivo, a la construcción de una ciudadanía responsable y a la formación de profesionales competentes para el mercado laboral. Si te apasiona trabajar con personas, transmitir conocimiento y contribuir a la construcción de un futuro mejor, la educación puede ser la carrera perfecta para ti. Te permitirá desarrollar habilidades altamente valoradas en el ámbito social y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos contextos educativos.',
      'foto': "../static/EDUCACION.jpg",
    },{
      'id': 8,
      'nombre': "Azafata",
      'descripcion':'La carrera de azafata es una profesión dinámica y llena de satisfacciones que te permite brindar atención de calidad y garantizar la seguridad de los pasajeros en vuelos comerciales. Las azafatas son como las embajadoras de la aerolínea a bordo, creando un ambiente agradable y acogedor para los pasajeros. Se encargan de asistirlos en sus necesidades, desde el embarque y desembarque hasta la entrega de equipaje y la resolución de dudas o inconvenientes. Además, son responsables de garantizar la seguridad de los pasajeros durante el vuelo. Realizan demostraciones de seguridad, asisten en caso de emergencias médicas y aplican los protocolos establecidos para mantener el orden y la tranquilidad a bordo. Si te gusta trabajar con personas, brindar un servicio de atención al cliente excepcional y tienes un espíritu aventurero, la carrera de azafata puede ser tu camino ideal. Te permitirá viajar por el mundo, conocer nuevas culturas y hacer la diferencia en la experiencia de vuelo de miles de personas.',
      'foto': "../static/AZAFATA.jpg",
    },{
      'id': 9,
      'nombre': "Relaciones Internacionales",
      'descripcion':'Las relaciones internacionales son una carrera fascinante que se adentra en el complejo mundo de las interacciones entre países, organizaciones internacionales, empresas transnacionales y otros actores globales. Su objetivo es comprender, analizar y abordar los desafíos y oportunidades que surgen en un mundo cada vez más interconectado. Los profesionales en relaciones internacionales son como diplomáticos e investigadores a la vez. Se especializan en áreas como la política internacional, la economía global, el derecho internacional, la seguridad internacional y la cooperación internacional. Su trabajo es fundamental para promover la paz, la seguridad, el desarrollo y la cooperación entre las naciones. Si te apasiona el mundo globalizado, te interesa comprender diferentes culturas y perspectivas, y deseas contribuir a un mundo más justo y pacífico, las relaciones internacionales pueden ser la carrera ideal para ti.Te permitirá desarrollar habilidades analíticas, de comunicación intercultural y de negociación, y te preparará para una amplia gama de carreras en el ámbito internacional,tanto en el sector público como en el privado.',
      'foto': "../static/RELACIONES_INTERNACIONALES.jpg",
    },{
      'id': 10,
      'nombre': "Arquitectura",
      'descripcion':'La administración de empresas es una carrera dinámica que se centra en la gestión eficiente de organizaciones para alcanzar sus objetivos. Abarca diversas áreas, desde la planificación estratégica hasta la gestión de recursos humanos y operaciones.En esencia, los administradores de empresas son los arquitectos del éxito de una organización. Planifican, organizan, dirigen y controlan los recursos para optimizar su funcionamiento y alcanzar metas establecidas.Es una carrera con alta demanda en el mercado laboral actual, ofreciendo oportunidades en diversos sectores y niveles jerárquicos..',
      'foto': "../static/ARQUITECTURA.jpg",
    },{
      'id': 11,
      'nombre': "Diseño de Modas",
      'descripcion':'El diseño de modas es una carrera vibrante y creativa que se centra en la concepción, creación y desarrollo de prendas de vestir, calzado y accesorios. Es un campo que combina la expresión artística con la comprensión de las tendencias del mercado, las propiedades de los materiales y las técnicas de confección. Los diseñadores de moda son como los artistas del mundo de la indumentaria. Transforman ideas en piezas tangibles que reflejan estilos, culturas y épocas. Su trabajo abarca desde el diseño inicial de bocetos y la selección de telas hasta la confección de prototipos y la presentación de colecciones en pasarelas o eventos de moda. Si te apasiona la moda, la creatividad y la expresión personal, el diseño de modas puede ser la carrera ideal para ti. Te permitirá desarrollar tu talento artístico, adquirir habilidades técnicas y convertirte en un agente de cambio en la industria de la moda.',
      'foto': "../static/DISEÑO_DE_MODAS.jpg",
    },{
      'id': 12,
      'nombre': "Ciencias de la Comunicación",
      'descripcion':'Las ciencias de la comunicación son un campo de estudio dinámico y apasionante que explora la creación, el intercambio y el consumo de información en diversos contextos. Abarca una amplia gama de disciplinas, desde la comunicación interpersonal y la publicidad hasta el periodismo y la producción audiovisual. Los profesionales de las ciencias de la comunicación son como los arquitectos del mensaje. Utilizan su creatividad, habilidades analíticas y conocimiento de los medios para comunicar ideas de manera efectiva, influir en la opinión pública y conectar a las personas entre sí. Su trabajo es crucial para informar, educar y entretener a la sociedad en un mundo cada vez más interconectado. Si te apasiona la comunicación, la tecnología y la cultura, las ciencias de la comunicación pueden ser la carrera perfecta para ti. Te permitirá desarrollar habilidades altamente valoradas en el mercado laboral y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos sectores, como la publicidad, el periodismo, las relaciones públicas, la producción audiovisual y la educación.',
      'foto': "../static/CIENCIAS_DE_LA_COMUNICACION.jpg",
    },{
      'id': 13,
      'nombre': "Producción Musical",
      'descripcion':'La producción musical es una carrera vibrante y creativa que se centra en la creación, grabación, edición y mezcla de música para diversos propósitos. Abarca desde la composición original hasta la masterización final, involucrando una amplia gama de habilidades técnicas y artísticas. En esencia, los productores musicales son los arquitectos del sonido. Dan vida a las ideas musicales, transformando melodías, ritmos y armonías en grabaciones profesionales que cautivan a las audiencias. Su trabajo es fundamental en la industria musical actual, participando en la creación de música para diversos medios, como álbumes de estudio, bandas sonoras de películas y videojuegos, publicidad, y presentaciones en vivo. Si te apasiona la música, la tecnología y la creatividad, la producción musical puede ser la carrera perfecta para ti. Te permitirá desarrollar habilidades técnicas y artísticas altamente valoradas, y te abrirá las puertas a un mundo de oportunidades en la emocionante industria musical.',
      'foto': "../static/PRODUCCION_MUSICAL.jpg",
    },{
      'id': 14,
      'nombre': "Diseño de Interiores",
      'descripcion':'La administración de empresas es una carrera dinámica que se centra en la gestión eficiente de organizaciones para alcanzar sus objetivos. Abarca diversas áreas, desde la planificación estratégica hasta la gestión de recursos humanos y operaciones.En esencia, los administradores de empresas son los arquitectos del éxito de una organización. Planifican, organizan, dirigen y controlan los recursos para optimizar su funcionamiento y alcanzar metas establecidas.Es una carrera con alta demanda en el mercado laboral actual, ofreciendo oportunidades en diversos sectores y niveles jerárquicos..',
      'foto': "../static/DIESÑO_DE_INTERIORES.jpg",
    },{
      'id': 15,
      'nombre': "Assesoria de imagen",
      'descripcion':'La asesoría de imagen es una carrera fascinante que te permite guiar a las personas en su camino hacia una imagen personal y profesional coherente, atractiva y efectiva. Como asesor de imagen, serás el confidente que los ayuda a descubrir su estilo único, resaltar sus fortalezas y comunicar su esencia a través de la apariencia, el comportamiento y la comunicación no verbal. A través de un análisis profundo de la imagen actual del cliente, sus objetivos y su estilo personal, desarrollarás un plan estratégico personalizado. Este plan incluirá recomendaciones de vestimenta, peinado, maquillaje, lenguaje corporal y etiqueta social, todo adaptado a las necesidades y preferencias del cliente. Tu labor como asesor de imagen no termina ahí. Brindarás apoyo y acompañamiento constante para que el cliente implemente el plan de acción de manera efectiva y sostenible, transformando su imagen y potenciando su éxito en todos los ámbitos de su vida. Si te apasiona ayudar a las personas a proyectar la mejor versión de sí mismas, la asesoría de imagen te ofrece una oportunidad única para desarrollar habilidades valiosas, marcar una diferencia en la vida de los demás y disfrutar de una carrera gratificante y llena de posibilidades.',
      'foto': "../static/ADMINISTRACION_DE_EMPRESAS.jpg",
    },{
      'id': 16,
      'nombre': "Manicurista",
      'descripcion':'La manicura es una carrera estética que se centra en el cuidado y embellecimiento de las uñas de manos y pies. Los manicuristas, como verdaderos artistas, utilizan su creatividad, habilidades técnicas y conocimiento de productos para transformar las uñas en pequeñas obras de arte. Su labor abarca desde la preparación de las uñas, incluyendo limpieza, limado, forma y cuidado de cutículas, hasta la aplicación de diversos esmaltes y la creación de diseños decorativos utilizando técnicas como el nail art, la aerografía y la aplicación de elementos decorativos. Los manicuristas también ofrecen servicios de cuidado de manos y pies, como hidratación, exfoliación y masajes, para mejorar la apariencia y el bienestar de sus clientes. Si te apasiona la belleza, el cuidado personal y la creatividad, la manicura puede ser una carrera ideal para ti. Te permitirá desarrollar habilidades altamente valoradas en el mercado laboral y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos sectores, como salones de belleza, centros comerciales, trabajo independiente, industria cosmética y docencia.',
      'foto': "../static/ADMINISTRACION_DE_EMPRESAS.jpg",
    },{
      'id': 17,
      'nombre': "Diseño Gráfico",
      'descripcion':'El diseño gráfico es una carrera creativa y dinámica que se centra en la comunicación visual. Los diseñadores gráficos son como narradores visuales que utilizan elementos como imágenes, colores, formas y tipografía para transmitir ideas, mensajes y emociones de manera efectiva a través de diversos medios. En esencia, los diseñadores gráficos son los encargados de traducir ideas en imágenes que impacten y comuniquen de manera clara y atractiva. Trabajan en una amplia gama de proyectos, desde el diseño de logotipos y empaques hasta la creación de páginas web y campañas publicitarias. Si te apasiona la creatividad, la comunicación y la idea de crear imágenes que impacten, el diseño gráfico puede ser la carrera perfecta para ti.Te permitirá desarrollar habilidades altamente valoradas en el mercado laboral y te abrirá las puertas a un sinfín de oportunidades profesionales en diversos sectores.',
      'foto': "../static/ADMINISTRACION_DE_EMPRESAS.jpg",
    },{
      'id': 18,
      'nombre': "Medicina Humanada",
      'descripcion':'La carrera de Medicina Humana es una profesión noble y desafiante que se centra en el estudio,diagnóstico,tratamiento y prevención de las enfermedades en el ser humano.Los médicos,como verdaderos guardianes de la salud,emplean su conocimiento científico,habilidades clínicas y compasión para cuidar el bienestar de sus pacientes. Si te apasiona la ciencia, la salud humana y ayudar a los demás, la medicina humana puede ser una carrera ideal para ti. Esta carrera te permitirá desarrollar habilidades altamente valoradas en el mercado laboral, te brindará la oportunidad de hacer una diferencia real en la vida de las personas y te permitirá disfrutar de una carrera gratificante y llena de satisfacciones.',
      'foto': "../static/ADMINISTRACION_DE_EMPRESAS.jpg",
    },{
      'id': 19,
      'nombre': "Pediatria",
      'descripcion':'La pediatría es una especialidad médica dedicada al cuidado integral de la salud de los niños desde el nacimiento hasta la adolescencia. Los pediatras, como verdaderos expertos en el desarrollo infantil, se enfocan en la prevención, el diagnóstico y el tratamiento de las enfermedades físicas, mentales y emocionales que afectan a los infantes y jóvenes. Si te apasiona la salud infantil,el desarrollo de los niños y ayudar a los más pequeños a crecer sanos y felices,la pediatría puede ser una carrera ideal para ti.Esta carrera te permitirá desarrollar habilidades altamente valoradas en el mercado laboral,te brindará la oportunidad de hacer una diferencia real en la vida de los niños y sus familias,y te permitirá disfrutar de una carrera gratificante y llena de satisfacciones.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 20,
      'nombre': "Obstetricia",
      'descripcion':'La carrera de Obstetricia se enfoca en el cuidado integral de la salud sexual y reproductiva de la mujer, la familia y la comunidad. Se encarga del embarazo, parto, puerperio y cuidado del recién nacido, brindando atención médica, psicológica y social durante todo el proceso. Las obstetras/os también educan en salud sexual y reproductiva, promueven la planificación familiar y la anticoncepción, y realizan investigaciones para mejorar la salud materna e infantil. Es una carrera con un alto grado de compromiso social y humano, ideal para personas con vocación de servicio, empatía y habilidades para el trabajo en equipo',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 21,
      'nombre': "Enfermeria",
      'descripcion':'La carrera de Enfermería se enfoca en la formación de profesionales capacitados para brindar atención integral de salud a individuos, familias y comunidades. Abarca el estudio de las bases científicas, biológicas y sociales que sustentan el cuidado de la salud, así como el desarrollo de habilidades técnicas y clínicas para la promoción, prevención, recuperación y rehabilitación de la salud. Los egresados en Enfermería pueden desempeñarse en diversos ámbitos del sector salud, como hospitales, clínicas, centros de salud, instituciones educativas, organismos públicos y privados, entre otros. En esencia, la carrera de Enfermería te prepara para ser un agente fundamental en el cuidado de la salud y el bienestar de las personas.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 22,
      'nombre': "Cosmetologia",
      'descripcion':'La cosmetología es una carrera técnica o profesional que se enfoca en el cuidado de la piel, el cabello y las uñas, promoviendo su salud y belleza. Los cosmetólogos adquieren conocimientos sobre anatomía, fisiología, química cosmética, dermatología y cosmetología estética para realizar tratamientos faciales y corporales, aplicar maquillaje, realizar manicuras y pedicuras, y asesorar a sus clientes sobre productos y cuidados adecuados para su tipo de piel y cabello. Es una carrera con alta demanda laboral en diversos ámbitos, como spas, clínicas estéticas, salones de belleza, centros de bienestar, la industria cosmética y como asesores independientes.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 23,
      'nombre': "Quimica Farmaceutica",
      'descripcion':'La carrera de Química Farmacéutica se enfoca en el estudio de los principios químicos, biológicos y farmacéuticos para el desarrollo, producción, análisis y control de medicamentos, cosméticos, productos alimenticios y otros productos de importancia para la salud. Los profesionales en esta área poseen amplios conocimientos en química orgánica e inorgánica, bioquímica, farmacología, análisis químico, tecnología farmacéutica y legislación farmacéutica, lo que les permite desempeñarse en diversos campos como la investigación y desarrollo de nuevos fármacos, la fabricación de medicamentos y productos sanitarios, el control de calidad en laboratorios, la atención farmacéutica en farmacias y hospitales, y la docencia en instituciones educativas. En resumen, la Química Farmacéutica es una carrera con un gran impacto en la salud y el bienestar de la población, ofreciendo a sus egresados múltiples oportunidades profesionales para contribuir al cuidado de la salud y el desarrollo de nuevos productos que mejoren la calidad de vida.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 24,
      'nombre': "Veterinaria",
      'descripcion':'La carrera de Medicina Veterinaria y Zootecnia se enfoca en la salud y el bienestar animal. Abarca un amplio espectro de conocimientos, desde la anatomía y fisiología animal hasta la prevención, diagnóstico y tratamiento de enfermedades. Los médicos veterinarios también se encargan de la producción animal sostenible, la seguridad alimentaria y la salud pública veterinaria. En resumen, la carrera veterinaria combina la ciencia con la pasión por los animales, preparando a profesionales para cuidar la salud animal en diversos ámbitos, desde clínicas y hospitales hasta la industria alimentaria y la conservación de la vida silvestre.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 25,
      'nombre': "Nutricion",
      'descripcion':'La carrera de Nutrición y Dietética, también conocida como Licenciatura en Nutrición, se enfoca en el estudio de la alimentación y su impacto en la salud humana. Los profesionales en esta área se encargan de evaluar las necesidades nutricionales de las personas, diseñar planes de alimentación personalizados, promover hábitos alimenticios saludables y educar sobre la importancia de una dieta balanceada para prevenir enfermedades y mejorar la calidad de vida. En otras palabras, los nutricionistas son expertos en alimentación que ayudan a las personas a comer de manera saludable para mantenerse sanas y prevenir enfermedades.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 26,
      'nombre': "Ingeniería de Sistemas",
      'descripcion':'La Ingeniería de Sistemas se enfoca en el diseño, análisis, desarrollo, implementación y mantenimiento de sistemas informáticos complejos que satisfagan las necesidades de las organizaciones. Los ingenieros de sistemas son profesionales capacitados para integrar hardware, software, redes y recursos humanos para crear soluciones tecnológicas eficientes y seguras. Su trabajo abarca desde la identificación de problemas y oportunidades de mejora en los procesos organizacionales, hasta la creación de sistemas a medida que optimicen la productividad, la toma de decisiones y la comunicación interna. En resumen, la carrera de Ingeniería de Sistemas prepara a profesionales para ser los arquitectos y gestores de la transformación digital en las empresas e instituciones.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 27,
      'nombre': "Ingenieria Mecatronica",
      'descripcion':'La Ingeniería Mecatrónica es una disciplina multidisciplinaria que combina la mecánica, la electrónica, la informática y los sistemas de control para diseñar, desarrollar, implementar y mantener sistemas inteligentes. Los ingenieros mecatrónicos se encargan de integrar estos diferentes campos para crear productos y procesos automatizados, desde robots y máquinas herramienta hasta dispositivos médicos y sistemas de transporte. En esencia, la carrera se enfoca en la creación de soluciones tecnológicas innovadoras que mejoren la eficiencia, la productividad y la calidad de vida en diversos sectores, como la industria manufacturera, la automotriz, la aeroespacial, la médica y la robótica. Si te apasiona la tecnología, la automatización y la resolución de problemas complejos, la Ingeniería Mecatrónica podría ser la carrera ideal para ti.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 28,
      'nombre': "Ingeniería Quimica",
      'descripcion':'La Ingeniería Química se encarga de transformar materias primas en productos útiles mediante procesos físicos, químicos y bioquímicos. Los ingenieros químicos aplican sus conocimientos de química, física, matemáticas y biología para diseñar, desarrollar, optimizar y gestionar estos procesos. Su trabajo tiene un impacto en diversos sectores, como la industria alimentaria, farmacéutica, petroquímica, textil, minera y de materiales. También pueden enfocarse en la investigación y desarrollo de nuevos productos y procesos, la gestión ambiental, la seguridad industrial y la biotecnología. En resumen, la Ingeniería Química es una carrera desafiante y versátil que ofrece una amplia gama de oportunidades profesionales para aquellos que buscan contribuir al desarrollo de productos y procesos que mejoren la vida de las personas.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 29,
      'nombre': "Ingenieria Mecanica",
      'descripcion':'La Ingeniería Mecánica es una disciplina que se enfoca en el diseño, análisis, fabricación y mantenimiento de sistemas mecánicos. Los ingenieros mecánicos utilizan principios de física, matemáticas y ciencia de materiales para crear máquinas, herramientas, dispositivos y procesos industriales. Su campo de trabajo es amplio e incluye desde el diseño de motores y turbinas hasta la creación de prótesis ortopédicas y sistemas de energía renovable. En resumen, la Ingeniería Mecánica es una carrera versátil que permite a los profesionales tener un impacto significativo en el mundo que nos rodea.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 30,
      'nombre': "Ingeniería Civil",
      'descripcion':'La Ingeniería Civil se enfoca en el diseño, construcción, mantenimiento y operación de infraestructuras que son esenciales para el desarrollo de la sociedad. Abarca una amplia gama de proyectos, desde edificios y puentes hasta carreteras, sistemas de agua y alcantarillado, aeropuertos, presas y túneles. Los ingenieros civiles utilizan su conocimiento en matemáticas, física, ciencias naturales y tecnología para crear soluciones innovadoras y sostenibles a los desafíos que enfrenta la sociedad. Es una carrera versátil y desafiante que ofrece muchas oportunidades para el crecimiento profesional. Si te apasiona la construcción, el diseño y la resolución de problemas, la Ingeniería Civil podría ser la carrera perfecta para ti.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
    },{
      'id': 31,
      'nombre': "Maquinaria Pesada",
      'descripcion':'La carrera de Maquinaria Pesada se enfoca en la formación de profesionales técnicos y/o ingenieros especializados en la operación, mantenimiento, reparación y gestión de equipos pesados utilizados en diversos sectores, como la construcción, minería, silvicultura y agricultura. Los planes de estudio comprenden desde la teoría fundamental de motores, sistemas hidráulicos, transmisiones y electricidad, hasta prácticas intensivas en el manejo y operación de excavadoras, bulldozers, grúas, retroexcavadoras y otras máquinas pesadas. Los egresados de esta carrera se desempeñan como operadores, técnicos de mantenimiento, supervisores o gerentes en empresas constructoras, mineras, contratistas y talleres especializados en maquinaria pesada.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
     },{
      'id': 32,
      'nombre': "Carrera Militar",
      'descripcion':'La carrera militar es una trayectoria profesional dentro de las Fuerzas Armadas, donde las personas sirven a su país y se capacitan para desempeñar diversas funciones en defensa de la nación. Esta carrera ofrece oportunidades de crecimiento personal, formación académica y desarrollo profesional, permitiéndoles a los individuos adquirir habilidades en liderazgo, estrategia, trabajo en equipo y manejo de situaciones complejas. Los interesados en una carrera militar deben cumplir con ciertos requisitos, como ser ciudadanos peruanos, tener una buena condición física y mental, y aprobar exámenes médicos, psicológicos y de aptitud. La carrera militar ofrece diversos beneficios, como estabilidad laboral, atención médica, planes de vivienda y oportunidades de especialización en diferentes áreas. Si te apasiona servir a tu país, defender los valores nacionales y desarrollar habilidades únicas, la carrera militar puede ser una excelente opción para ti..',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
     },{
      'id': 33,
      'nombre': "Carrera Oficial",
      'descripcion':'La Carrera Oficial es un recorrido preestablecido por el que transitan todas las cofradías que participan en las procesiones de Semana Santa en diversas localidades españolas. Este trayecto, que suele incluir calles y plazas emblemáticas del centro histórico, tiene un carácter oficial y religioso, ya que las cofradías realizan allí su estación de penitencia ante la Catedral o iglesia mayor. La Carrera Oficial se ha convertido en un elemento fundamental de la Semana Santa en España, concentrando a un gran número de fieles y espectadores que desean presenciar el fervor y la devoción de las cofradías. Además, este recorrido oficial ofrece la posibilidad de disfrutar de una visión completa de la procesión, ya que por allí pasan todas las cofradías participantes. Cabe destacar que la Carrera Oficial no solo tiene un valor religioso, sino también cultural e histórico, ya que forma parte de las tradiciones y costumbres de las diferentes localidades donde se celebra la Semana Santa.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
     },{
      'id': 34,
      'nombre': "Ingenieria de Sistemnas",
      'descripcion':'La Agronomía es una carrera que se enfoca en el estudio, la gestión y la optimización de los procesos de producción agrícola y ganadera. Se encarga de aplicar conocimientos científicos y tecnológicos para cultivar la tierra de manera eficiente y sostenible, con el objetivo de obtener alimentos y otros productos de primera necesidad. Los ingenieros agrónomos, profesionales egresados de esta carrera, trabajan en diversos ámbitos, desde el manejo de cultivos y el cuidado del ganado hasta la agroindustria y la investigación. Su labor es fundamental para garantizar la seguridad alimentaria y el desarrollo rural. En resumen, la Agronomía es una carrera que combina ciencia, tecnología y pasión por el campo, con un gran potencial para impactar positivamente en el mundo.',
      'foto': "../static/INGENIERIA_DE_SISTEMAS.jpg",
     })
    for profession in professiones:
        if(profession.get("id")==idResultado):
            nombre=profession.get("nombre")
            descripcion=profession.get("descripcion")
            direccionFoto=profession.get("foto")
            break
    return nombre,descripcion,direccionFoto

def devolverTop(rango,x):
    subconjunto = []
    contador=1
    for numero in rango:
        if numero != x and contador<=3:
            subconjunto.append(numero)
        contador+=1
    return subconjunto
    
def mejoresCarreras(resultado):
    subconjunto = []
    contador=1
    if(resultado>=1 and resultado<=4):
        rango = (1, 2, 3, 4)
        return devolverTop(rango,resultado)
    elif(resultado>=5 and resultado<=9):
        rango = (6, 5, 7, 8, 9)
        return devolverTop(rango,resultado)
    elif(resultado>=10 and resultado<=17):
        rango = (10, 12, 11, 16, 17,13,14,15)
        return devolverTop(rango,resultado)
    elif(resultado>=18 and resultado<=25):
        rango = (18, 19, 20, 21, 24, 25,22,23 )
        return devolverTop(rango,resultado)
    elif(resultado>=18 and resultado<=25):
        rango = (18, 19, 20, 21, 24, 25,22,23 )
        return devolverTop(rango,resultado)
    elif(resultado>=26 and resultado<=31):
        rango = (26, 30, 29, 27, 28, 31)
        return devolverTop(rango,resultado)
    elif(resultado>=32 and resultado<=33):
        rango = (32, 33, 29, 27, 28, 31)
        return devolverTop(rango,resultado)
    else:
        return (34)


def entrenamientoModelo():
    df=pd.read_csv("respuestasoficiales.csv" , encoding='latin-1')
    x_train=df.iloc[:,0:14]
    y_train=df.iloc[:,14:15]
    modelo=svm.SVC()
    modelo.fit(x_train,y_train.values.ravel())
    return modelo

def prediccion(modelo,sumaInteres,sumaAptitudes):
    x_test=pd.DataFrame({'CI':sumaInteres[0],'HI':sumaInteres[1],'AI':sumaInteres[2],'SI':sumaInteres[3],'II':sumaInteres[4],'DI':sumaInteres[5],'EI':[6],'CA':sumaAptitudes[0],'HA':sumaAptitudes[1],'AA':sumaAptitudes[2],'SA':sumaAptitudes[3],'IA':sumaAptitudes[4],'DA':sumaAptitudes[5],'EA':[6]})
    return modelo.predict(x_test)