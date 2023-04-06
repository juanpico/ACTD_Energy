<h1 align="center"> Proyecto 2 - Analítica Computacional para la toma de decisiones </h1>
<h1 align="center"> Pronóstico de series de tiempo </h1>
<p align="left">
   <img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green">
</p>

## Descripción 🚀
Este repositorio incluye el despliegue del proyecto 2 del curso Analítica Computacional para la toma de decisiones del Departamento de Ingeniería Industrial de la Universidad de los Andes.

Este proyecto tiene como objetivo desarrollar un proyecto de analítica de datos para la predicción de una serie de tiempo.

Concretamente, se decidió utilizar los datos de la carga total en Austria en MW según lo publicado en ENTSO-E Transparency Platform. Estos datos fueron obtenidos de: [Open Power System Data](https://data.open-power-system-data.org/time_series/2020-10-06)

La estructura del proyecto se divide en 3 componentes:
1. Análisis de datos: El análisis realizado se encuentra en el notebook "ETL hourly.ipynb".
2. Modelo: La estimación del modelo SARIMA utilizado para modelar la serie de tiempo se realiza en el archivo "modelo.ipynb"
3. Dashboard: Se realizó un dashboard como herramienta de apoyo a la decisión mediante Dash. Esta herramienta fue desplegada en una maquina virtual. El código y los soportes de la herramienta se encuentran en la carpeta "Dashboard".

## Construido con :wrench: :hammer:
* [Python](https://www.python.org)
* [Dash](https://dash.plotly.com)
* [statsmodels](https://www.statsmodels.org/stable/index.html)

## Previsualización del Dashboard

<img width="1431" alt="image" src="https://user-images.githubusercontent.com/75444742/230502417-1516b48b-057a-4158-bcb0-27e2f4bff516.png">


## Autores :raised_hands:
* Mauricio Ricardo Delgado (<mr.delgado@uniandes.edu.co>)
* Juan Camilo Pico (<jc.picog@uniandes.edu.co>)

## Disclaimer
Este proyecto esta en sus primeras etapas de desarrollo. Todos los errores son atribuites a los autores. Apreciamos cualquier aporte para mejorar el contenido.
