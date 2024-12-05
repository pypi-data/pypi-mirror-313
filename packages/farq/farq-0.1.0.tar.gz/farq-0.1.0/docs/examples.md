# Examples

## Basic Water Detection

```python
import farq

# Load bands
green, meta = farq.read("landsat_green.tif")
nir, _ = farq.read("landsat_nir.tif")

# Calculate NDWI
ndwi = farq.ndwi(green, nir)

# Create water mask and calculate statistics
water_mask = ndwi > 0
water_pixels = farq.sum(water_mask)
water_percentage = (water_pixels / water_mask.size) * 100

print(f"Water coverage: {water_percentage:.1f}%")

# Visualize results
farq.plot(ndwi, title="NDWI Analysis", cmap="RdYlBu", vmin=-1, vmax=1)
farq.plt.show()
```

## Temporal Change Analysis

```python
import farq
import os

# Load data for two time periods
base_dir = "examples/chad_lake"

# 1985 data
green_85, _ = farq.read(os.path.join(base_dir, "1985", "LT05_L2SP_185051_19850501_20200918_02_T1_SR_B2.TIF"))
nir_85, _ = farq.read(os.path.join(base_dir, "1985", "LT05_L2SP_185051_19850501_20200918_02_T1_SR_B4.TIF"))

# 2024 data
green_24, _ = farq.read(os.path.join(base_dir, "2024", "LC08_L2SP_185051_20230323_20230404_02_T1_SR_B3.TIF"))
nir_24, _ = farq.read(os.path.join(base_dir, "2024", "LC08_L2SP_185051_20230323_20230404_02_T1_SR_B5.TIF"))

# Resample 2024 data to match 1985 dimensions
green_24 = farq.resample(green_24, green_85.shape)
nir_24 = farq.resample(nir_24, nir_85.shape)

# Calculate NDWI for both periods
ndwi_85 = farq.ndwi(green_85, nir_85)
ndwi_24 = farq.ndwi(green_24, nir_24)

# Calculate water coverage for each period
water_mask_85 = ndwi_85 > 0
water_percentage_85 = (farq.sum(water_mask_85) / water_mask_85.size) * 100

water_mask_24 = ndwi_24 > 0
water_percentage_24 = (farq.sum(water_mask_24) / water_mask_24.size) * 100

# Print results
print(f"1985 Water coverage: {water_percentage_85:.2f}%")
print(f"2024 Water coverage: {water_percentage_24:.2f}%")
print(f"Change in coverage: {water_percentage_24 - water_percentage_85:.2f}%")

# Visualize comparison
farq.compare(ndwi_85, ndwi_24,
    title1="NDWI 1985",
    title2="NDWI 2024",
    cmap="RdYlBu",
    vmin=-1, vmax=1)
farq.plt.show()
```

## Multi-Index Analysis

```python
import farq

# Load all required bands
bands = {
    'blue': farq.read("landsat_blue.tif")[0],
    'green': farq.read("landsat_green.tif")[0],
    'red': farq.read("landsat_red.tif")[0],
    'nir': farq.read("landsat_nir.tif")[0]
}

# Calculate multiple indices
ndvi = farq.ndvi(bands['red'], bands['nir'])
ndwi = farq.ndwi(bands['green'], bands['nir'])
evi = farq.evi(bands['red'], bands['nir'], bands['blue'])

# Calculate coverage statistics
veg_mask = ndvi > 0.2
veg_percentage = (farq.sum(veg_mask) / veg_mask.size) * 100

water_mask = ndwi > 0
water_percentage = (farq.sum(water_mask) / water_mask.size) * 100

# Print results
print(f"Vegetation coverage: {veg_percentage:.1f}%")
print(f"Water coverage: {water_percentage:.1f}%")

# Visualize indices
farq.plot(ndvi, title="NDVI Analysis", cmap="RdYlGn", vmin=-1, vmax=1)
farq.plt.show()

farq.plot(ndwi, title="NDWI Analysis", cmap="RdYlBu", vmin=-1, vmax=1)
farq.plt.show()

farq.plot(evi, title="EVI Analysis", cmap="RdYlGn", vmin=-1, vmax=1)
farq.plt.show()
```

## Band Statistics

```python
import farq

# Load a band
data, meta = farq.read("landsat_band.tif")

# Calculate basic statistics
print(f"Min: {farq.min(data):.2f}")
print(f"Max: {farq.max(data):.2f}")
print(f"Mean: {farq.mean(data):.2f}")
print(f"Standard deviation: {farq.std(data):.2f}")

# Visualize the band
farq.plot(data, title="Band Data", cmap="viridis")
farq.plt.show()
``` 