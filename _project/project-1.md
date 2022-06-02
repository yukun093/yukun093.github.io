---
title: "AviGuardX"
excerpt: "Drone detection with neural network to avoid collision with plane<br/><img src='/images/AviGuardX.png'>"
permalink: /project/project-1/
videourl: 'https://yukun093.github.io/files/AviGuardX.mp4'
collection: project
---

------

At airports safety is everything. As the number of drones and unmanned aerial vehicles increases, it’s crucial for airports to identify objects in the sky. The amount of bird strikes has also been on the rise, which shows how important it is to detect objects before it’s too late.

This project was sponsored by Isaware and the initial goal was to apply space technology in aviation industry, and after the first discussions with Isaware Oy we identified the potential of using neural networks technology to identify objects that could cause harm in the airspace, e.g., drones and birds. Next, we evaluated many different available methods to track flying object, e.g. using infrared cameras, active radar, passive radar or acoustic detection.

Finally, considering the feasibility, cost as well as difficulty, the plan using passive radar is adopted. One the one hand, passive radar could reduce the cost to purchase active large radar detection system. At the other hand, the detection system would be used at night as well and it should be covered within 3km. After computation of bistatic radar equation which is SNR, we achieved the result of 4-5kms of detection area that the radar could achieve.

When it comes to model selection, in this project, we use Faster RCNN to classify and recognize the drones and flying birds as targets. Though the current CNN model is developing rapidly, and improved algorithms suitable for various applications emerge in endlessly, the premise is to construct different types of datasets. The completeness namely diversity, and the accuracy of annotation for detection object, namely selected areas, directly determine the final output accuracy.

Also, there is one video link(https://yukun093.github.io/files/AviGuardX.mp4), which is made by one of my teammate, Genesis Mateo from Thomas Jefferson University, to explain how the whole process we have experienced.