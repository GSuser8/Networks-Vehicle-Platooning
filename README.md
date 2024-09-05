# Enhanced Vehicle Platooning with Sliding Window RLNC Technique
Vehicle Platooning with Sliding Window and RLNC Technique combines flow control and error resilience mechanisms to enhance communication between vehicles in a platoon. In vehicle platooning, multiple vehicles move together, often with close spacing, where communication plays a vital role in maintaining coordination, speed, and safety.
- Sliding Window Protocol: Controls data flow by limiting packets sent before waiting for acknowledgment, preventing network congestion.
- RLNC (Random Linear Network Coding): Encodes packets for error resilience, allowing vehicles to recover data even if some packets are lost.
  
## Enhancements introduced:
 1. Congestion Control and Avoidance using Additive Increase and Multiplicative Decrease Algorithm.
 2. Synchronization of communication between vehicles.

## Running the code:

To run the main code, run the following command

```bash
  python vehiclePlatoon.py
```

## References:
Base paper:
[Vehicle Platooning with Sliding Window RLNC Technique](https://drive.google.com/file/d/132Tv154_KG6EUpcnoUk2YeHps87DvKGl/view?usp=drivesdk)


## Contributers:
- [Stuti Poddar](https://github.com/Stuti-Poddar)
- [Gauri Sankaran N.](https://github.com/GSuser8)
