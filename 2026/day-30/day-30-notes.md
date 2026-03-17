# What are layers?

Layers are snapshots of filesystem changes, stacked on top of each other to form a complete image. Each Dockerfile instruction that touches files creates a new layer.

# Why does Docker use them?

Speed — rebuild only what changed, cache the rest
Efficiency — shared layers aren't duplicated on disk
Transparency — docker image history shows exactly what built the image and how much each step costs in size 
