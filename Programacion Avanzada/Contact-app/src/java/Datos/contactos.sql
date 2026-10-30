-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-05-2024 a las 18:39:37
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `contactos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos_familiares`
--

CREATE TABLE `contactos_familiares` (
  `id_familiares` int(55) NOT NULL,
  `nombre` varchar(55) NOT NULL,
  `apellido` varchar(55) NOT NULL,
  `celular` varchar(10) NOT NULL,
  `tipo_familiar` varchar(55) NOT NULL,
  `direccion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos_laborales`
--

CREATE TABLE `contactos_laborales` (
  `id_laborales` int(55) NOT NULL,
  `nombre` varchar(55) NOT NULL,
  `apellido` varchar(55) NOT NULL,
  `celular` varchar(10) NOT NULL,
  `posicion_laboral` varchar(55) NOT NULL,
  `segundo_numero` varchar(10) NOT NULL,
  `empresa` varchar(55) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos_negocios`
--

CREATE TABLE `contactos_negocios` (
  `id_negocios` int(55) NOT NULL,
  `nombre` varchar(55) NOT NULL,
  `apellido` varchar(55) NOT NULL,
  `celular` varchar(10) NOT NULL,
  `segundonumero` varchar(10) NOT NULL,
  `posicion_laboral` varchar(55) NOT NULL,
  `empresa` varchar(55) NOT NULL,
  `direccion_empresa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_usuarios`
--

CREATE TABLE `registros_usuarios` (
  `nombre` varchar(100) NOT NULL,
  `celular` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registros_usuarios`
--

INSERT INTO `registros_usuarios` (`nombre`, `celular`, `password`) VALUES
('daniel', '123123', '123123');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contactos_familiares`
--
ALTER TABLE `contactos_familiares`
  ADD PRIMARY KEY (`id_familiares`);

--
-- Indices de la tabla `contactos_laborales`
--
ALTER TABLE `contactos_laborales`
  ADD PRIMARY KEY (`id_laborales`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
