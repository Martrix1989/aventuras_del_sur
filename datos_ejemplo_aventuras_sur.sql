-- ============================================================
-- DATOS DE EJEMPLO: ECOPARQUE AVENTURAS DEL SUR
-- Compatible con el proyecto Django 6.0 entregado.
--
-- IMPORTANTE:
-- 1) Crear la base aventuras_sur.
-- 2) Ejecutar primero: python manage.py migrate
-- 3) Importar este archivo en MySQL Workbench seleccionando
--    la base aventuras_sur.
--
-- Cuentas de prueba (todas usan la clave: Aventura123!)
-- Administrador: admin
-- Guia 1:         guia1
-- Guia 2:         guia2
-- Turista 1:      turista1
-- Turista 2:      turista2
--
-- El archivo inserta registros en las tablas Django existentes.
-- No crea tablas ni reemplaza las migraciones.
-- ============================================================

USE aventuras_sur;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar únicamente los datos de ejemplo de estas tablas.
-- Se eliminan en orden para respetar las relaciones.
DELETE FROM experiencias_inscripcion;
DELETE FROM experiencias_experiencia;
DELETE FROM experiencias_categoria;
DELETE FROM cuentas_usuario;

-- ------------------------------------------------------------
-- 1. USUARIOS
-- ------------------------------------------------------------
USE aventuras_sur;
INSERT INTO cuentas_usuario
(id, password, last_login, is_superuser, username, first_name, last_name,
 email, is_staff, is_active, date_joined, rol)
VALUES
(1, 'pbkdf2_sha256$600000$AventurasSur2026$OeZ0lYs/6DsV5c1rraQQjrcfkEz7oMLZJeVnwD6gzfA=', NULL, 1, 'admin', 'Administrador', 'General',
 'admin@aventurasur.cl', 1, 1, '2026-11-10 12:00:00', 'admin'),
(2, 'pbkdf2_sha256$600000$AventurasSur2026$OeZ0lYs/6DsV5c1rraQQjrcfkEz7oMLZJeVnwD6gzfA=', NULL, 0, 'guia1', 'Camila', 'Rojas',
 'camila.rojas@aventurasur.cl', 0, 1, '2026-11-10 12:00:00', 'guia'),
(3, 'pbkdf2_sha256$600000$AventurasSur2026$OeZ0lYs/6DsV5c1rraQQjrcfkEz7oMLZJeVnwD6gzfA=', NULL, 0, 'guia2', 'Matías', 'González',
 'matias.gonzalez@aventurasur.cl', 0, 1, '2026-11-10 12:00:00', 'guia'),
(4, 'pbkdf2_sha256$600000$AventurasSur2026$OeZ0lYs/6DsV5c1rraQQjrcfkEz7oMLZJeVnwD6gzfA=', NULL, 0, 'turista1', 'Valentina', 'Pérez',
 'valentina.perez@correo.cl', 0, 1, '2026-11-10 12:00:00', 'turista'),
(5, 'pbkdf2_sha256$600000$AventurasSur2026$OeZ0lYs/6DsV5c1rraQQjrcfkEz7oMLZJeVnwD6gzfA=', NULL, 0, 'turista2', 'Diego', 'Muñoz',
 'diego.munoz@correo.cl', 0, 1, '2026-11-10 12:00:00', 'turista');

-- ------------------------------------------------------------
-- 2. CATEGORÍAS
-- ------------------------------------------------------------
USE aventuras_sur;
INSERT INTO experiencias_categoria
(id, nombre, descripcion, activo)
VALUES
(1, 'Trekking', 'Caminatas guiadas por senderos y paisajes naturales.', 1),
(2, 'Canopy', 'Recorridos en altura mediante cables y arneses de seguridad.', 1),
(3, 'Kayak', 'Navegación recreativa en kayak con equipo de seguridad.', 1),
(4, 'Arriendo de equipos', 'Equipamiento para actividades al aire libre.', 1);

-- ------------------------------------------------------------
-- 3. EXPERIENCIAS
-- Cada guía registra al menos cuatro experiencias.
-- Fechas futuras respecto de noviembre de 2026.
-- ------------------------------------------------------------
USE aventuras_sur;
INSERT INTO experiencias_experiencia
(id, titulo, descripcion, precio, cupo_maximo, fecha_hora, estado,
 creado_en, categoria_id, creador_id)
VALUES
(1, 'Trekking Sendero del Bosque',
 'Caminata guiada de dificultad baja por el bosque nativo. Incluye orientación y pausas interpretativas.',
 12000.00, 12, '2026-12-05 09:00:00', 1, '2026-11-10 12:00:00', 1, 2),
(2, 'Trekking Mirador del Sur',
 'Ascenso guiado hasta un mirador natural con vistas panorámicas. Dificultad media.',
 18000.00, 10, '2026-12-06 10:00:00', 1, '2026-11-10 12:00:00', 1, 2),
(3, 'Canopy Aventura',
 'Circuito de canopy con equipo de protección y charla de seguridad previa.',
 25000.00, 8, '2026-12-12 11:00:00', 1, '2026-11-10 12:00:00', 2, 2),
(4, 'Kayak Laguna Escondida',
 'Experiencia de kayak recreativo con instrucciones iniciales y acompañamiento de guía.',
 20000.00, 10, '2026-12-13 09:30:00', 1, '2026-11-10 12:00:00', 3, 2),

(5, 'Trekking Ruta de las Cascadas',
 'Recorrido guiado por senderos naturales hasta una zona de cascadas.',
 16000.00, 12, '2026-12-19 09:00:00', 1, '2026-11-10 12:00:00', 1, 3),
(6, 'Canopy Bosque Alto',
 'Circuito de canopy entre plataformas elevadas, con supervisión del operador.',
 28000.00, 8, '2026-12-20 10:00:00', 1, '2026-11-10 12:00:00', 2, 3),
(7, 'Kayak Río Tranquilo',
 'Salida de kayak por un tramo de aguas tranquilas, apta para principiantes.',
 22000.00, 10, '2026-12-26 09:30:00', 1, '2026-11-10 12:00:00', 3, 3),
(8, 'Arriendo Kit de Campamento',
 'Arriendo de equipo básico para disfrutar una jornada de campamento en el parque.',
 15000.00, 6, '2026-12-27 10:00:00', 1, '2026-11-10 12:00:00', 4, 3);

-- ------------------------------------------------------------
-- 4. INSCRIPCIONES / RESERVAS
-- Cada turista tiene al menos tres reservas.
-- ------------------------------------------------------------
USE aventuras_sur;
INSERT INTO experiencias_inscripcion
(id, fecha_inscripcion, estado_pago, experiencia_id, usuario_id)
VALUES
(1, '2026-11-10 12:10:00', 'confirmado', 1, 4),
(2, '2026-11-10 12:12:00', 'pendiente', 3, 4),
(3, '2026-11-10 12:15:00', 'confirmado', 5, 4),
(4, '2026-11-10 12:20:00', 'pendiente', 2, 5),
(5, '2026-11-10 12:22:00', 'confirmado', 6, 5),
(6, '2026-11-10 12:25:00', 'pendiente', 7, 5);

-- Ajustar AUTO_INCREMENT para que los siguientes registros
-- creados desde Django no choquen con los IDs de ejemplo.
USE aventuras_sur;
ALTER TABLE cuentas_usuario AUTO_INCREMENT = 6;
ALTER TABLE experiencias_categoria AUTO_INCREMENT = 5;
ALTER TABLE experiencias_experiencia AUTO_INCREMENT = 9;
ALTER TABLE experiencias_inscripcion AUTO_INCREMENT = 7;

SET FOREIGN_KEY_CHECKS = 1;

-- FIN DE LOS DATOS DE EJEMPLO
