---
title: "Exops-M2-Smart-Robot"
excerpt: "ArmMotus M2 upper extremity intelligent rehabilitation robot development<br/><img src='/images/Exops-m2-Smart-Robot.png'>"
permalink: /project/project-Exops-m2-smart-robot/
collection: project
---

------

It is one smart robot development project that i once joined in when i was an intern in the Fourier Intelligence. It should be also known that the cover image is from [fourier intelligence robot](https://www.fitness-gaming.com/news/health-and-rehab/fourier-m2-enhances-every-stage-of-neurological-rehabilitation.html).

At first, it is one project that finally is adopted to participate in one chinese AI competition of 5G. So when i worked with Dr. Nimos Liu, many working results already have been completed. For example, the M2 robot is run by several months and several contexts, such as P2P, Fitts, Money(recursive actions) and relatively difficult CarGame which are four medical actions. From the view of coding, much of scripts already created by previous interns, for example, drawing the result of curves to adjust the trajectory of arm's action which is come back from expos robot. In Unity 3d, several senarios have been already generated as well since that would spend almost one or two years until the normal operation. So in this position, what I have done is to maintain the connection with hardwares and softwares to keep it safe working and fix bugs if some parameters had been modified, such as running speed, running distance or running total running time. It also should be noted that this work is cooperated with Ruijin Hospital, Shanghai Jiaotong University School of Medicine.

After completing this project, i continued working with some researchers from The University of Melbourne to finish how to obtain the joint angles of the upper limb with the help of one motion capture equipment(Xsens). I once confronted many difficulties when i was working independently, for example, i am not fimiliar with prior programming language(C#), so outputing the result with the format of .csv from Unity3D seemed more difficult than using other programming languages. However, this problem finally is solved due to Xsens staff's help. And after achieving the .csv file, those data should be dealt with to present the suitable result with curves. Angle extraction algorithm is cited from this paper "VanLith 16 Calibration Free Upper Limb Joint Motion Estimation Algorithm with Wearable Sensors", and data extraction and curve drawing scripts are created by my working time with matlab.
