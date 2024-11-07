# Storage Bin Allocation Analysis for Optimized Picking Routes

![Warehouse Optimization](https://img.shields.io/badge/Warehouse-Optimization-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Problem Statement](#problem-statement)
- [Scenarios](#scenarios)
  - [Scenario A: Ascending Order Allocation](#scenario-a-ascending-order-allocation)
  - [Scenario B: Descending Access Frequency Allocation](#scenario-b-descending-access-frequency-allocation)
  - [Scenario C: Clustering Based on Common Removals](#scenario-c-clustering-based-on-common-removals)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Visualization](#visualization)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Efficient warehouse management is crucial for minimizing operational costs and enhancing productivity. This project analyzes the impact of different storage bin allocation strategies on picking routes within a warehouse setting. By simulating three distinct allocation scenarios, the study aims to determine the most effective method for reducing total picking distance, thereby optimizing the overall picking process.

## Features

- **Access Frequency Calculation:** Determines how often each item is picked across all orders.
- **Common Removal Analysis:** Identifies pairs of items frequently picked together to facilitate clustering.
- **Hierarchical Clustering:** Groups items based on common removal data using average linkage.
- **Picking Route Simulation:** Calculates total picking distances for different storage allocation scenarios.
- **Visualization:** (Optional) Visual representations of storage layouts for each scenario.

## Problem Statement

In a warehouse, items are stored in bins arranged linearly. An order picker retrieves items based on incoming orders, starting and ending at a base location (B). The objective is to allocate items to storage positions in a manner that minimizes the total distance the picker travels while fulfilling all orders.

### **Given:**

- **Items:** 10 articles numbered 1 through 10.
- **Storage Positions:** 10 positions arranged linearly, each 1 meter apart from the next.
- **Orders:** 50 picking orders, each specifying a subset of items to retrieve.

### **Scenarios:**

1. **Ascending Order Allocation:** Items are placed in storage positions in ascending numerical order.
2. **Descending Access Frequency Allocation:** Items are placed based on how frequently they are picked, with the most frequently picked items closest to the base.
3. **Clustering Based on Common Removals:** Items frequently picked together are clustered and arranged to optimize picking routes.

## Scenarios

### Scenario A: Ascending Order Allocation

**Description:** Items are assigned to storage positions in ascending numerical order (1 to 10). This straightforward approach does not consider picking frequency or item associations.

### Scenario B: Descending Access Frequency Allocation

**Description:** Items are allocated based on their access frequency. Items picked more frequently are placed closer to the base, reducing the distance the picker travels for common items.

### Scenario C: Clustering Based on Common Removals

**Description:** Items frequently picked together are grouped into clusters using hierarchical clustering with average linkage. Clusters are ordered based on total access frequencies, and items within clusters are ordered by their individual frequencies.

