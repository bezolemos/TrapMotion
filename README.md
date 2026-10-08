# TrapMotion

**TrapMotion** is a Python physics simulator developed to analyze the behavior of a mousetrap-powered car.

The project combines physics, mathematics, and programming to estimate how different design parameters affect the car's performance, including wheel diameter, axle diameter, string length, lever arm length, total mass, and spring characteristics.

## Features

- Geometry and theoretical range calculation
- Spring torque and energy analysis
- Force and acceleration calculations
- Rolling resistance
- Wheel traction limit
- Time-based movement simulation
- Target-distance verification
- Design diagnostics and recommendations
- Graphs for:
  - position
  - velocity
  - acceleration
  - spring angle
- Graphical interface built with Tkinter

## Project Structure

```text
TrapMotion/
├── simulador.py
├── interface_v11.py
├── simulacao.py
├── README.md
└── README_PT-BR.md
```

- `simulador.py` — main file used to start the application.
- `interface_v11.py` — contains the graphical interface and result visualization.
- `simulacao.py` — contains the physics calculations and simulation logic.

## Requirements

- Python 3.x
- Matplotlib

Install Matplotlib with:

```bash
py -m pip install matplotlib
```

## How to Run

Open the project folder in VS Code or a terminal and run:

```bash
py simulador.py
```

The graphical interface will open.

Then enter the car parameters and click **SIMULAR CARRINHO** to view the results, diagnostics, recommendations, and graphs.

## Project Goal

The goal of TrapMotion is to work as a support tool for the development of mousetrap-powered cars, allowing different configurations to be tested before physically building the vehicle.

Besides calculating results, the program also aims to help explain **why** specific design choices improve or limit the car's performance.

## Model Limitations

TrapMotion uses a simplified physical model.

The simulation considers rolling resistance and traction limits, but does not model every real-world effect in detail, such as:

- aerodynamic drag
- wheel rotational inertia
- weight distribution between axles
- detailed kinetic friction
- real wheel slip
- other mechanical losses

Therefore, the results should be treated as estimates to support the design process.

## Status

✅ **Final Version — Project 15**
