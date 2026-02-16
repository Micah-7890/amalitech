### A. The Executive Summary
* Our delivery audit reveals that customer dissatisfaction is strongly associated with inaccurate delivery estimates rather than isolated late shipments alone. While delivery delays occur nationwide, remote and infrastructure-constrained regions exhibit significantly higher late and super-late rates, suggesting regional logistical inefficiencies. More importantly, categories with higher delay percentages consistently show lower average review scores, confirming that over-promising and under-delivering materially impacts customer sentiment. The findings indicate that the issue is partially regional but also systemic in delivery time estimation accuracy. Addressing forecast reliability and improving logistics performance in high-risk regions and product categories will significantly improve customer satisfaction and brand trust.

### B. Project Links
* **Link to Notebook:** [link to repo](https://github.com/Micah-7890/amalitech)
* **Link to Dashboard:** [dashboard](https://logisticsappdashboard.streamlit.app/)
* **Link to Presentation:** [presentation](https://1drv.ms/p/c/08707647154fcc86/IQD55QkZg622SbF_8s2odme3Ad0tR6m_C3Pz1jNRHZO9mCY?e=xeaIzh)
### C. Technical Explanation
* The dataset was originally distributed across multiple relational CSV files. I first performed structured joins using the correct joins to create a unified master dataset for analysis.
The cleaning process included:
Converting date columns (order_delivered_customer_date, order_estimated_delivery_date) into proper datetime formats to enable accurate delay calculations.
Handling missing values by separating canceled and unavailable orders from delivered orders to prevent distortion in delivery performance metrics.
Creating a structured delivery classification system:
    Delivered
    Failed (canceled/unavailable)
    In Progress
Generating clean boolean flags (is_late, is_super_late) to simplify percentage calculations using mean aggregation.
These steps ensured consistent, reliable metrics for delay analysis and customer sentiment evaluation.

* To demonstrate analytical thinking beyond the core requirements, I introduced a Category-Level Risk Analysis Dashboard that connects operational delay performance with customer sentiment.
Specifically, I:
Calculated late delivery percentages by product category.
Linked those delay metrics to average review scores.
Built a quadrant-style bubble chart where:
X-axis = Late Delivery Percentage
Y-axis = Average Review Score
Bubble Size = Order Volume
This enhancement provides strategic business value because it identifies not just where delays occur, but where delays materially impact customer perception at scale. It enables leadership to prioritize operational improvements in high-volume, high-risk product segments.

**Important Note on Code Submission:**
* Upload your `.ipynb` notebook file to the repo.
* **Crucial:** Also upload an **HTML or PDF export** of your notebook so we can see your charts even if GitHub fails to render the notebook code.
* Once you are ready, please fill out the [Official Submission Form Here](https://forms.office.com/e/heitZ9PP7y) with your links

---

## 🛑 CRITICAL: Pre-Submission Checklist

**Before you submit your form, you MUST complete this checklist.**

> ⚠️ **WARNING:** If you miss any of these items, your submission will be flagged as "Incomplete" and you will **NOT** be invited to an interview. 
>
> **We do not accept "permission error" excuses. Test your links in Incognito Mode.**

### 1. Repository & Code Checks
- [✅] **My GitHub Repo is Public.** (Open the link in a Private/Incognito window to verify).
- [✅] **I have uploaded the `.ipynb` notebook file.**
- [✅] **I have ALSO uploaded an HTML or PDF export** of the notebook.
- [✅] **I have NOT uploaded the massive raw dataset.** (Use `.gitignore` or just don't commit the CSV).
- [✅] **My code uses Relative Paths.** 

### 2. Deliverable Checks
- [✅] **My Dashboard link is publicly accessible.** (No login required).
- [✅] **My Presentation link is publicly accessible.** (Permissions set to "Anyone with the link can view").
- [✅] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness
- [✅] I have completed **User Stories 1-4**.
- [✅] I have completed the **"Candidate's Choice"** challenge and explained it in the README.

**✅ Only when you have checked every box above, proceed to the submission form.**

---
