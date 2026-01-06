-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 03-07-2025 a las 13:47:21
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mealmate`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('8d3xj9cf40tq36g15sq0jb4owqy5rxzk', 'eyJ1YmljYWNpb24iOiIxMC4zNTM5Mjk3NzY5ODA1NzErLTY2Ljk2NzMyNDAxODQ3ODQxIn0:1tw9rG:OXHvlfsLPEGs7eV7OuTbqod3xlVFCCdTckdVMmbNtM0', '2025-04-06 01:10:34.910301'),
('3ynb8l4coo1v3hx1nykv5g8q8r1i2x4f', 'eyJ1YmljYWNpb24iOiIxMC4zMzcyMzg3NTQzOTM2OTIrLTY3LjA5MzQwOTE3NzM5NjExIn0:1to9i9:u_nU7LxZRsRzuowgNxo4G3VUlnh5__cqkoPPxEb8Jxg', '2025-03-14 23:24:05.509944'),
('c368lbn7eak2t73chsjt4kqnplisqezd', 'eyJidXNxdWVkYSI6ImN1cGFja2UiLCJyZXN0YXVyYW50ZSI6NiwidWJpY2FjaW9uIjoiMTAuMzM4MzUxNDkyOTYzMjc4Ky02Ny4wOTM3NTI2MjI2MDQzOCJ9:1uGLfo:BJ22zFmbIMvK0HdwvvoYlqRVjgyo_o_Msj0Tsa3J09Q', '2025-05-31 17:50:12.574386'),
('znbmn3yjfszdaqlz0iq9inv6ihbvpqt6', '.eJwNy8EOgyAMANB_6XWOAJNWOe1XOtIDiYjBEk2W_fu4v_eF_smJU647RHDWzKtDnANZ8nZd_OOJaGhxL49EFoMLHibQfFSI2rpMIIXzNu55iehbbi7HJibVMlyTU7k33lUg4u8PaSAgRg:1tb1zs:gqBYzNZS8PNTLFz1bo218GcqRKC97F_3SRZZuFYYotc', '2025-02-06 18:32:08.819240');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_pagoefectivo`
--

DROP TABLE IF EXISTS `pedidos_pagoefectivo`;
CREATE TABLE IF NOT EXISTS `pedidos_pagoefectivo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `monto` double NOT NULL,
  `billetes` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedidos_pagoefectivo_pedido_id_c218e4ca` (`pedido_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos_pagoefectivo`
--

INSERT INTO `pedidos_pagoefectivo` (`id`, `pedido_id`, `monto`, `billetes`) VALUES
(6, 18, 2.32, '0,1,0,0,0,0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_pagomovil`
--

DROP TABLE IF EXISTS `pedidos_pagomovil`;
CREATE TABLE IF NOT EXISTS `pedidos_pagomovil` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `banco` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `monto` double NOT NULL,
  `ref` int NOT NULL,
  `titular` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio_dolar` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedidos_pagomovil_pedido_id_4bb5d55f` (`pedido_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos_pagomovil`
--

INSERT INTO `pedidos_pagomovil` (`id`, `pedido_id`, `banco`, `monto`, `ref`, `titular`, `telefono`, `precio_dolar`) VALUES
(6, 16, '0102', 11.6, 324242, 'Carla', '13333333333', 55.7611),
(5, 15, '0102', 11.6, 7777, 'Carla', '13333333333', 55.7611),
(7, 17, '0151', 23.2, 76788779, 'Carlos', '13333333333', 55.7611);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_paypalmodel`
--

DROP TABLE IF EXISTS `pedidos_paypalmodel`;
CREATE TABLE IF NOT EXISTS `pedidos_paypalmodel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `monto` double NOT NULL,
  `ref` int NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `titular` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio_dolar` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedidos_paypalmodel_pedido_id_95a3d4a9` (`pedido_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_pedidomodel`
--

DROP TABLE IF EXISTS `pedidos_pedidomodel`;
CREATE TABLE IF NOT EXISTS `pedidos_pedidomodel` (
  `nro_items` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `notas` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `cantidades` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `nombre` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `identificacion` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `ubicacion` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `status` tinyint(1) NOT NULL,
  `monto` double NOT NULL,
  `is_delivery` tinyint(1) NOT NULL,
  `is_pickup` tinyint(1) NOT NULL,
  `nro` int NOT NULL AUTO_INCREMENT,
  `id_nro_id` int NOT NULL,
  `puntodeventa_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`nro`),
  KEY `pedidos_pedidomodel_id_nro_id_3e6df338` (`id_nro_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos_pedidomodel`
--

INSERT INTO `pedidos_pedidomodel` (`nro_items`, `fecha`, `notas`, `cantidades`, `nombre`, `identificacion`, `email`, `telefono`, `ubicacion`, `status`, `monto`, `is_delivery`, `is_pickup`, `nro`, `id_nro_id`, `puntodeventa_active`) VALUES
('7', '2025-01-24 02:11:00.000000', 'Vacio.', '1', 'Carla', '23232321', 'carla@example.com', '13333333333', 'No aplica', 0, 11.6, 0, 1, 14, 5, 0),
('7', '2025-01-23 04:11:00.000000', 'Vacio.', '1', 'Carla', '23232321', 'carla@example.com', '13333333333', 'No aplica', 0, 11.6, 0, 1, 15, 5, 0),
('7', '2025-01-24 03:13:00.000000', 'Vacio.', '1', 'Carla', '23232321', 'carla@example.com', '13333333333', 'No aplica', 0, 11.6, 0, 1, 16, 5, 0),
('7', '2025-01-23 16:22:00.000000', 'Vacio.', '2', 'Carla', '23232321', 'carla@example.com', '13333333333', 'No aplica', 0, 23.2, 0, 1, 17, 5, 0),
('8', '2025-01-23 16:23:07.190092', 'Vacio.', '1', 'ewew', '323213', 'ewe@gmail.com', '32332333333', 'No aplica', 0, 2.32, 0, 1, 18, 5, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_zellemodel`
--

DROP TABLE IF EXISTS `pedidos_zellemodel`;
CREATE TABLE IF NOT EXISTS `pedidos_zellemodel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `monto` double NOT NULL,
  `ref` int NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `titular` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio_dolar` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedidos_zellemodel_pedido_id_ddee10ac` (`pedido_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_pickup_delivery`
--

DROP TABLE IF EXISTS `servicios_pickup_delivery`;
CREATE TABLE IF NOT EXISTS `servicios_pickup_delivery` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `p_start_time` time(6) NOT NULL,
  `p_end_time` time(6) NOT NULL,
  `active_pickup` tinyint(1) NOT NULL,
  `d_start_time` time(6) NOT NULL,
  `d_end_time` time(6) NOT NULL,
  `active_delivery` tinyint(1) NOT NULL,
  `restaurante_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `servicios_pickup_delivery_restaurante_id_c56c4c90` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios_pickup_delivery`
--

INSERT INTO `servicios_pickup_delivery` (`id`, `p_start_time`, `p_end_time`, `active_pickup`, `d_start_time`, `d_end_time`, `active_delivery`, `restaurante_id`) VALUES
(3, '00:00:00.000000', '23:50:00.603000', 1, '10:00:00.000000', '20:00:00.000000', 1, 5),
(4, '07:00:00.000000', '22:30:00.000000', 1, '08:00:00.000000', '17:00:00.000000', 1, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_reservaciones_config`
--

DROP TABLE IF EXISTS `servicios_reservaciones_config`;
CREATE TABLE IF NOT EXISTS `servicios_reservaciones_config` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mesas` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `restaurante_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `servicios_reservaciones_config_restaurante_id_455133bb` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios_reservaciones_config`
--

INSERT INTO `servicios_reservaciones_config` (`id`, `mesas`, `active`, `restaurante_id`) VALUES
(3, '10,8,2,4', 1, 5),
(4, '7,4,3,6', 1, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_reservaciones_horario`
--

DROP TABLE IF EXISTS `servicios_reservaciones_horario`;
CREATE TABLE IF NOT EXISTS `servicios_reservaciones_horario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mesa` int NOT NULL,
  `fecha` date NOT NULL,
  `horas` varchar(288) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `restaurante_id` int NOT NULL,
  `status` varchar(144) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `servicios_reservaciones_horario_restaurante_id_82a7edee` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_reservacion_cliente`
--

DROP TABLE IF EXISTS `servicios_reservacion_cliente`;
CREATE TABLE IF NOT EXISTS `servicios_reservacion_cliente` (
  `nro_reserva` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `identificacion` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `mesa` int NOT NULL,
  `nro_personas` int NOT NULL,
  `restaurante_id` int NOT NULL,
  PRIMARY KEY (`nro_reserva`),
  KEY `servicios_reservacion_cliente_restaurante_id_0204aca6` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_cliente`
--

DROP TABLE IF EXISTS `user_r_cliente`;
CREATE TABLE IF NOT EXISTS `user_r_cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(18) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `password` varchar(128) NOT NULL,
  `cedula` varchar(8) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(11) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `user_r_cliente`
--

INSERT INTO `user_r_cliente` (`id`, `username`, `nombre`, `password`, `cedula`, `email`, `telefono`, `last_login`, `is_active`, `date_joined`) VALUES
(1, 'carla2', 'Carla', '323dwdwddw', '23232321', 'carla@example.com', '13333333333', '2025-01-23 15:47:44.093879', 0, '2025-01-22 05:15:45.428123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_ingredientes`
--

DROP TABLE IF EXISTS `user_r_ingredientes`;
CREATE TABLE IF NOT EXISTS `user_r_ingredientes` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `ingrediente` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_ingredientes`
--

INSERT INTO `user_r_ingredientes` (`codigo`, `ingrediente`) VALUES
(1, 'Tomate'),
(2, 'Lechuga'),
(3, 'Sal'),
(4, 'Queso americano'),
(5, 'Pimienta'),
(6, 'Harina de trigo'),
(7, 'Carne de res'),
(8, 'Carne de cerdo'),
(9, 'Leche'),
(10, 'Azúcar morena'),
(24, 'Durazno'),
(23, 'Miel'),
(22, 'Queso'),
(21, 'Piña'),
(25, 'Tocineta'),
(26, 'Zanahoria'),
(27, 'Pasta'),
(28, 'Chocolate');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_menu`
--

DROP TABLE IF EXISTS `user_r_menu`;
CREATE TABLE IF NOT EXISTS `user_r_menu` (
  `comida` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `precios` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `codigo` varchar(360) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `item` int NOT NULL AUTO_INCREMENT,
  `restaurante_id` int NOT NULL,
  `img` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`item`),
  KEY `user_r_menu_restaurante_id_1daa4564` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_menu`
--

INSERT INTO `user_r_menu` (`comida`, `precios`, `codigo`, `item`, `restaurante_id`, `img`) VALUES
('Macarrones con queso', '10', '5,22,4,3,25', 7, 5, NULL),
('Sushi', '2', '21,25', 8, 5, 'comida/maki.jpg'),
('Pizza', '12', '6', 9, 5, ''),
('Hamburguesa', '5', '6', 10, 5, ''),
('Galletas de chocolate', '3', '6,9,23', 13, 6, ''),
('Cupcake', '2', '24,6,9,23', 14, 6, ''),
('Helado de chocolate', '3', '10', 15, 6, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_pago`
--

DROP TABLE IF EXISTS `user_r_pago`;
CREATE TABLE IF NOT EXISTS `user_r_pago` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pagomovil_active` tinyint(1) NOT NULL,
  `banco` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono_pm` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `efectivo_active` tinyint(1) NOT NULL,
  `restaurante_id` int NOT NULL,
  `punto_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_r_pago_restaurante_id_7cb5f495` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_pago`
--

INSERT INTO `user_r_pago` (`id`, `pagomovil_active`, `banco`, `telefono_pm`, `efectivo_active`, `restaurante_id`, `punto_active`) VALUES
(3, 1, '0134', '32323232323', 1, 5, 1),
(4, 1, '0128', '04127687687', 1, 6, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_paypal`
--

DROP TABLE IF EXISTS `user_r_paypal`;
CREATE TABLE IF NOT EXISTS `user_r_paypal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `paypal_active` tinyint(1) NOT NULL,
  `nombre` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `user` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `correo` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `phone_p` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `restaurante_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_r_paypal_restaurante_id_2cb1d047` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_paypal`
--

INSERT INTO `user_r_paypal` (`id`, `paypal_active`, `nombre`, `user`, `correo`, `phone_p`, `restaurante_id`) VALUES
(3, 1, 'Mac&Cheese', 'maccheeese', 'macadncheese@example.com', '03828323333', 5),
(4, 1, 'Sweet\'s', 'sweet', 'sweet@gmail.com', '04127986968', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_restaurante`
--

DROP TABLE IF EXISTS `user_r_restaurante`;
CREATE TABLE IF NOT EXISTS `user_r_restaurante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `username` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rif` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `direccion` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `fundacion` date NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_r_restaurante_email_b4f23f80_uniq` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_restaurante`
--

INSERT INTO `user_r_restaurante` (`id`, `nombre`, `username`, `rif`, `email`, `telefono`, `direccion`, `fundacion`, `last_login`, `is_active`, `date_joined`, `logo`, `password`) VALUES
(5, 'Mac&Cheese', 'maccheese', '33333333333344298422', 'macadncheese@example.com', '02776735263', '10.474835606609721+-66.76254272460939+20', '2023-06-22', '2025-01-23 16:18:36.110170', 0, '2025-01-22 22:07:49.861073', 'restaurantes/rest1.jpg', '23e2e2e'),
(6, 'Sweet', 'sweet', '38299380293802333333', 'sweet@example.com', '33323424244', '10.474835606609721+-66.76254272460939', '2021-07-14', '2025-05-17 17:43:21.763135', 0, '2025-01-23 16:37:34.788447', 'restaurantes/postres2.jpg', 'pbkdf2_sha256$870000$WMvZ6MneqqGb7LHnaOCsrq$FWc7JmtxDJWuf4EsfyV2TdxPqi9zhQ/86crrLvoyy88=');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_r_zelle`
--

DROP TABLE IF EXISTS `user_r_zelle`;
CREATE TABLE IF NOT EXISTS `user_r_zelle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `zelle_active` tinyint(1) NOT NULL,
  `mail_z` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `phone_z` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `restaurante_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_r_zelle_restaurante_id_7bfa33d3` (`restaurante_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_r_zelle`
--

INSERT INTO `user_r_zelle` (`id`, `zelle_active`, `mail_z`, `phone_z`, `restaurante_id`) VALUES
(2, 1, 'macadncheese@example.com', '23232333333', 5),
(3, 1, 'swett@gmail.com', '05631738111', 6);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
