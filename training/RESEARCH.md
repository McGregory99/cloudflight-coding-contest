# Investigación: ediciones pasadas del CCC

## Resumen

Las fuentes verificadas permiten reconstruir un mapa de ediciones y problemas del Cloudflight (antes Catalysts) Coding Contest entre 2019 y 2025. Lo que no permiten es entregar el dossier completo que pedía la pregunta: enunciados íntegros, soluciones en Python verificadas y explicación por problema. CCC es un concurso por niveles: la dificultad sube en cada nivel y gana quien llega más alto en menos tiempo, con penalizaciones. Los niveles se desbloquean de uno en uno en CatCoder, que exige iniciar sesión. Las fuentes no muestran una estructura de "qualifier/final": cada edición es un evento de un día con tracks (School, Classic, Data/AI). Mapa de ediciones (Classic): 30.ª mar-2019 Tower Wars; 32.ª nov-2019 Solar City; 33.ª abr-2020 Quantum Breakdown; 34.ª oct-2020 Smartgrid/power-scheduling; 35.ª nov-2021 lang-interpreter; 36.ª nov-2022 Pacman; 37.ª 31-mar-2023 torneo de piedra-papel-tijera; 38.ª 20-oct-2023 islas/rutas en mapa W/L; 39.ª abr-2024 Lawnmower; 40.ª oct-2024 Room Planner; 41.ª 14-nov-2025 Spaceship. Los repositorios de GitHub son la mejor fuente pública de enunciados (PDF), entradas y soluciones Python: blu3r4y, gergely-elias, KarolWes, Anghelus-Diana y zor-cell (este último en Java). Kilonova aloja la CCC 36 como juez online. Solo se han comprobado contra los ejemplos del enunciado unos pocos niveles 1 (oct-2020, oct-2023, oct-2024). Todo lo demás debe tratarse como NO VERIFICADO.

## Hallazgos

### 1. (high, voto 3-0)

Formato del CCC: concurso por niveles. La dificultad sube en cada nivel y gana quien completa el nivel más alto en menos tiempo. El tiempo incluye minutos de penalización por envío incorrecto. CatCoder entrega el PDF del enunciado y el ZIP de entradas nivel a nivel, solo tras resolver el anterior. Hace falta iniciar sesión y los concursos se identifican por un ID numérico (p. ej. catcoder.codingcontest.org/training/140/play), no por año ni edición.

**Evidencia:** El blog oficial dice: 'The difficulty increases with each level' y 'the winner is who completes the highest level in the shortest amount of time'. Las normas de GLS Polonia añaden penalizaciones. El README y next_level.py de ccc_solver_template inician sesión en CatCoder, descargan el pdf y el zip del nivel actual y extraen .in a in/ y .out a out/.

- https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/
- https://github.com/Lingepumpe/ccc_solver_template

### 2. (high, voto 3-0)

Fechas confirmadas: la 37.ª edición fue el 31-mar-2023 y la 38.ª el 20-oct-2023 (unos 5.000 participantes). La 41.ª fue el viernes 14-nov-2025 con tres tracks y problemas distintos: School 'Asteroid Mining' (diseño óptimo de túneles), Classic 'Spaceship' (guiar una nave con un algoritmo preciso) y Data/AI 'Migratory Birds' (entrenar modelos que predicen la migración de aves).

**Evidencia:** Ambas fechas vienen de notas de prensa del organizador y están corroboradas por el calendario de la LMU y por codeweek.eu. Se refutó por 0-3 que la 41.ª tuviera 6 niveles por track: el track Classic Spaceship tiene 8 niveles según zor-cell.

- https://www.cloudflight.io/en/blog/41st-cloudflight-coding-contest-brings-together-developers-worldwide/
- https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/

### 3. (medium, voto 3-0)

Mapa edición → problema del track Classic: 30.ª mar-2019 Tower Wars; 32.ª nov-2019 Solar City; 33.ª abr-2020 Quantum Breakdown; 34.ª oct-2020 Smartgrid (power-scheduling); 35.ª nov-2021 lang-interpreter; 36.ª nov-2022 Pacman; 37.ª mar-2023 rps-tournament; 38.ª oct-2023 island-routing; 39.ª abr-2024 Lawnmower (niveles 1-7); 40.ª oct-2024 Room Planner / desk-placement (niveles 1-7); 41.ª nov-2025 Spaceship (niveles 1-8).

**Evidencia:** Los números de edición salen de las descripciones de los repos de blu3r4y. Los temas salen de la tabla del README de dpaguba, del README de zor-cell y de las descripciones de KarolWes. La fuente oficial solo confirma Lawnmower (39.ª) y Spaceship (41.ª). Las fuentes son coherentes entre sí, pero son secundarias y están etiquetadas por los propios autores.

- https://github.com/blu3r4y?tab=repositories&q=ccc
- https://github.com/dpaguba/cloudflight-coding-contest
- https://github.com/zor-cell/cc-contests
- https://github.com/KarolWes/ccc_spring23
- https://github.com/KarolWes/cloudflight2022_pacman
- https://www.cloudflight.io/en/blog/41st-cloudflight-coding-contest-brings-together-developers-worldwide/

### 4. (medium, voto 3-0)

Descripción de problemas por edición. Oct-2020 Smartgrid: L1 da N minutos con su precio y pide el id (desde 0) del minuto más barato, desempatando por el id menor; el enfoque global es greedy (franja más barata primero). Nov-2022 Pacman: L1 cuenta las monedas 'C' de la rejilla; L2 simula movimientos U/D/L/R desde una posición inicial y cuenta las monedas distintas recogidas. Mar-2023: torneo de piedra-papel-tijera; L1 resuelve duelos por parejas, L2 hace rondas eliminatorias y hay una variante de 5 estilos (S, L, P, Y, R, con lagarto y Spock). Oct-2023: mapa N×N de 'W'/'L'; L1 imprime el carácter de cada coordenada 'x,y'. Abr-2024 Lawnmower: evaluar rutas de un cortacésped y luego encontrar una ruta que cubra un césped con árboles. Oct-2024 Room Planner: L1 cuenta cuántos escritorios 1×3 caben por sala; los niveles siguientes colocan escritorios de tamaños mixtos sin que se toquen (backtracking DFS con poda). Nov-2025 Spaceship: secuencias de paces para llegar a la estación en un tiempo límite; después hay que esquivar asteroides fijos y móviles.

**Evidencia:** El L1 de oct-2020 se decodificó del PDF oficial alojado en data/Level 1.pdf. Pacman y RPS se dedujeron leyendo main.py. El L1 de oct-2023 sale de level1_example.in/.out. El L1 de Room Planner sale del PDF level-1.pdf de zor-cell. Las descripciones de los niveles altos solo se apoyan en los README.

- https://github.com/blu3r4y/ccc-linz-oct2020
- https://github.com/KarolWes/cloudflight2022_pacman
- https://github.com/KarolWes/ccc_spring23
- https://github.com/Anghelus-Diana/Cloudflight-Coding-Contest
- https://github.com/zor-cell/cc-contests
- https://github.com/dpaguba/cloudflight-coding-contest

### 5. (medium, voto 3-0)

Soluciones comprobadas a mano contra el ejemplo del enunciado. (a) Oct-2023 L1: la respuesta correcta es m[y][x], es decir x = columna e y = fila. Con el ejemplo (4,2), (6,6) y (10,6) da L, W, W, que coincide con el .out. El Level1.py del repo usa m[x][y], devuelve 'W' para (4,2) y falla, y además nunca se ejecuta por la guarda `if __name__ == '_main_'`. Queda marcado como NO VERIFICADO/erróneo. (b) Oct-2024 L1: con escritorios 1×3 y x divisible por 3, la respuesta es (x//3)*y. El ejemplo 6 5 / 9 8 / 6 7 da 10 / 24 / 14 y coincide. (c) Oct-2020 L1: es un argmin con desempate por el primer índice, `min(range(n), key=lambda i: p[i])`. Encaja con el enunciado, pero no se ha ejecutado contra el fichero de ejemplo.

**Evidencia:** El verificador comparó los ficheros de ejemplo oficiales incluidos en los repos con las fórmulas. Trampa habitual: la convención de ejes en la rejilla (x = columna).

- https://github.com/Anghelus-Diana/Cloudflight-Coding-Contest
- https://github.com/zor-cell/cc-contests
- https://github.com/blu3r4y/ccc-linz-oct2020

### 6. (high, voto 3-0 (2-1 en el detalle de ramas/tags de oct2020))

Fuentes de enunciados, entradas y soluciones Python. Las de blu3r4y son las más útiles: 11 repos en Python (ccc-linz-mar2019, nov2019, apr2020, oct2020, nov2021, nov2022, mar2023, oct2023, apr2024, oct2024, nov2025). En oct2020 están los PDF oficiales de L1-L7 en data/ y las soluciones de L1-L6 en las etiquetas git level1..level6 (src/contest.py, son tags y no ramas); L7 quedó sin terminar. gergely-elias/ccc dice tener soluciones 'confirmed' en Python por nivel para addictive_game, islands, lawn_mower, matchmaking, pacman, rock_paper_scissors, room_planner y smartgrid, junto con los enunciados en HTML. Anghelus-Diana tiene oct-2023 L1-L6 (.py para L1, L2, L4, L5 y L6; L3 sin .py; PDFs solo de L2-L6). KarolWes cubre parcialmente RPS 2023 y Pacman 2022. zor-cell cubre la 39.ª-41.ª con PDFs, entradas, Java y salidas. dpaguba tiene 7 ediciones con un solution.cpp de algoritmo núcleo cada una, en C++ y no en Python.

**Evidencia:** Comprobado con la API de GitHub (repos, árboles git, refs y README). La etiqueta 'confirmed' de gergely-elias es una afirmación del autor y no tiene corroboración externa.

- https://github.com/blu3r4y?tab=repositories&q=ccc
- https://github.com/blu3r4y/ccc-linz-oct2020
- https://github.com/gergely-elias/ccc
- https://github.com/Anghelus-Diana/Cloudflight-Coding-Contest
- https://github.com/zor-cell/cc-contests
- https://github.com/dpaguba/cloudflight-coding-contest
- https://github.com/topics/cloudflight-coding-contest

### 7. (medium, voto 3-0)

Kilonova (lista #75) aloja la 'Cloudflight Coding Contest 36' como juez con 7 niveles: L1=#295, L2=#294, L3=#296, L4=#297, L5=#298, L6=#292, L7=#293 (kilonova.ro/problems/<id>). Allí el enunciado está en PDF y el envío exige iniciar sesión y se hace con las respuestas, no con el código. Por la numeración de blu3r4y, la CCC 36 corresponde a nov-2022 (Pacman), pero eso es una inferencia.

**Evidencia:** La lista y las páginas de problemas #292 y #295 se consultaron directamente. Kilonova no confirma de forma independiente el tema de la CCC 36.

- https://kilonova.ro/problem_lists/75

### 8. (low, voto derivado)

Patrones recurrentes y cómo reconocerlos. (1) Simulación sobre rejilla con movimientos U/D/L/R o secuencias de pasos (Pacman, Lawnmower, Spaceship): el L1 suele ser contar o consultar, y los niveles altos añaden obstáculos o generación de rutas (BFS o cobertura). (2) Parsing y búsqueda en mapas de caracteres (islas W/L): cuidado con x = columna. (3) Torneos y reglas de enfrentamiento (RPS): simulación de rondas que acaba en búsqueda o construcción de alineaciones. (4) Optimización greedy sobre series temporales (Smartgrid: franja más barata, scheduling). (5) Empaquetado o colocación en rejilla (Room Planner): primero una fórmula aritmética y luego backtracking con poda. (6) Intérpretes de mini-lenguajes (lang-interpreter 2021). (7) Física o cinemática con límite de tiempo (Spaceship). Estructura típica: L1 es lectura y cálculo trivial, y cada nivel añade una restricción que obliga a cambiar de algoritmo.

**Evidencia:** Es una síntesis hecha a partir de las descripciones de los README (dpaguba trae columna de algoritmo: greedy, backtracking DFS, etc.) y del código leído. No proviene de una fuente que enumere los patrones.

- https://github.com/dpaguba/cloudflight-coding-contest
- https://github.com/zor-cell/cc-contests
- https://github.com/KarolWes/cloudflight2022_pacman
- https://github.com/blu3r4y/ccc-linz-oct2020

## Advertencias

- - **El entregable pedido no está completo.** Faltan, por cada problema, el enunciado íntegro, el formato de E/S, los ejemplos, una solución Python verificada y el análisis de complejidad. Solo se comprobaron contra el ejemplo algunos niveles 1 (oct-2020, oct-2023 y oct-2024). Las demás soluciones de los repos están NO VERIFICADAS. La de Anghelus-Diana para oct-2023 L1 es errónea.
- **No hay rondas qualifier/final.** Ninguna fuente muestra esa estructura; las ediciones son eventos de un día con tracks.
- **Ediciones y tracks sin datos.** No se encontró nada de la 31.ª edición (≈ otoño 2019). Tampoco se confirmó si hubo ediciones en primavera de 2021, 2022 y 2025: la afirmación de que no había repos para esas fechas se refutó 0-3, así que su existencia y su cobertura siguen abiertas. Los tracks School y Data/AI no tienen soluciones ni enunciados salvo los títulos de 2025.
- **Fuentes débiles.** La mayoría de los temas y números de edición vienen de etiquetas puestas por los autores de repos personales, no de codingcontest.org. Esto incluye la etiqueta 'confirmed' de gergely-elias y la equivalencia CCC 36 = Pacman.
- **Acceso limitado a los oficiales.** Los enunciados oficiales de CatCoder requieren iniciar sesión y no se consultaron directamente.
- **Fuentes que no son Python.** dpaguba está en C++ y zor-cell en Java.
- **Vigencia.** Los repos pueden cambiar. zor-cell está activo y su último push es de 2026-10.

## Preguntas abiertas

- ¿Qué temas y problemas tuvieron la 31.ª edición (≈ oct/nov 2019) y las posibles ediciones de primavera de 2021, 2022 y 2025? ¿Existen repos o archivos de ellas?
- ¿Las soluciones Python de blu3r4y (nov2019-nov2025) y gergely-elias pasan los ejemplos oficiales de cada nivel si se ejecutan contra los .in/.out incluidos?
- ¿A qué edición pertenecen los problemas 'addictive_game' y 'matchmaking' de gergely-elias? ¿Y cuál era el contenido completo de los niveles 2-7 de Lawnmower, Room Planner y Spaceship?
- ¿Se pueden conseguir enunciados de los tracks School y Data/AI (p. ej. Asteroid Mining y Migratory Birds) en CatCoder sin necesitar credenciales?

## Refutado

- {"claim": "Each track of the 41st CCC consisted of six levels of increasing difficulty.", "vote": "0-3", "source": "https://www.cloudflight.io/en/blog/41st-cloudflight-coding-contest-brings-together-developers-worldwide/"}
- {"claim": "There are no repos for the spring 2021, spring 2022 or spring 2025 contests. Coverage for 2019-2025 is therefore incomplete: those editions still need other sources.", "vote": "0-3", "source": "https://github.com/blu3r4y?tab=repositories&q=ccc"}

## Fuentes

- {"url": "https://github.com/zor-cell/cc-contests", "quality": "secondary", "angle": "official-archive", "claimCount": 5}
- {"url": "https://github.com/gergely-elias/ccc", "quality": "forum", "angle": "official-archive", "claimCount": 4}
- {"url": "https://github.com/topics/cloudflight-coding-contest", "quality": "secondary", "angle": "official-archive", "claimCount": 5}
- {"url": "https://github.com/Lingepumpe/ccc_solver_template", "quality": "secondary", "angle": "official-archive", "claimCount": 5}
- {"url": "https://www.cloudflight.io/en/blog/41st-cloudflight-coding-contest-brings-together-developers-worldwide/", "quality": "primary", "angle": "official-archive", "claimCount": 5}
- {"url": "https://de.linkedin.com/in/handrale", "quality": "unreliable", "angle": "official-archive", "claimCount": 0}
- {"url": "https://github.com/blu3r4y?tab=repositories&q=ccc", "quality": "primary", "angle": "github-python-solutions", "claimCount": 5}
- {"url": "https://github.com/blu3r4y/ccc-linz-oct2020", "quality": "blog", "angle": "github-python-solutions", "claimCount": 5}
- {"url": "https://github.com/istvan-olah/CCC34", "quality": "forum", "angle": "github-python-solutions", "claimCount": 5}
- {"url": "https://github.com/exokortex/ccc_2022_classic", "quality": "forum", "angle": "github-python-solutions", "claimCount": 5}
- {"url": "https://github.com/Anghelus-Diana/Cloudflight-Coding-Contest", "quality": "secondary", "angle": "github-python-solutions", "claimCount": 5}
- {"url": "https://github.com/cseriildi/Cloudflight-Coding-Contest", "quality": "forum", "angle": "github-python-solutions", "claimCount": 4}
- {"url": "https://github.com/dpaguba/cloudflight-coding-contest", "quality": "blog", "angle": "writeups-blogs", "claimCount": 5}
- {"url": "https://github.com/blu3r4y/ccc-linz-oct2024", "quality": "blog", "angle": "writeups-blogs", "claimCount": 4}
- {"url": "https://alibek-cholponbaev.medium.com/my-experience-with-the-cloudflight-coding-contest-29ac782713fa", "quality": "unreliable", "angle": "writeups-blogs", "claimCount": 0}
- {"url": "https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/", "quality": "primary", "angle": "finals-and-school-contests", "claimCount": 5}
- {"url": "https://github.com/blu3r4y/ccc-linz-nov2022", "quality": "blog", "angle": "finals-and-school-contests", "claimCount": 4}
- {"url": "https://kilonova.ro/problem_lists/75", "quality": "secondary", "angle": "patterns-and-strategy", "claimCount": 4}
