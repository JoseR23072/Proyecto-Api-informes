-- Insertar en Batida
INSERT IGNORE INTO Batida (id, nombre, latitud, longitud, id_zona, estado, fecha_evento, descripcion)
VALUES 
(1, 'Batida Río Segura', 38.345, -0.481, 1, FALSE, '2024-06-01', 'Recogida de basura en el río.'),
(2, 'Batida Parque Central', 39.4699, -0.3763, 2, FALSE, '2024-06-02', 'Limpieza del parque central.');

-- Insertar en BatidaVoluntario
INSERT IGNORE INTO BatidaVoluntario (id_batida, id_voluntario)
VALUES 
(1, 1),
(1, 2),
(2, 1);