# 🚨 CANADIAN MEDICAL DEVICE HAZARD REPORTING COLUMNS EXPLAINED

## 📋 **What the Canadian Database Tells Us About Device Hazards**

The Canadian Medical Device Incidents Database has **17 columns** that capture different aspects of device problems. Here's what each hazard-related column shows:

---

## 🎯 **KEY HAZARD COLUMNS**

### **1. 📝 INCIDENT_TYPE_E/F (English/French)**
**What it shows:** How the problem was reported

- **Voluntary problem report** (348 cases) - Hospitals/companies reported voluntarily
- **Mandatory problem report** (239 cases) - Required by law to report
- **Summary mandatory reports** (1 case) - Grouped reports

**💡 Why this matters:** Mandatory reports suggest more serious problems

---

### **2. 🚨 HAZARD_SEVERITY_CODE_E/F (English/French)**
**What it shows:** How dangerous the incident was

- **DEATH** (1 case) - Device caused death
- **POTENTIAL FOR DEATH/INJURY** (224 cases) - Could have killed/injured
- **INJURY** (17 cases) - Actually injured patient  
- **MINIMAL/NO ADVERSE HEALTH CONSEQUENCES** (344 cases) - Minor/no harm
- **UNASSIGNED** (2 cases) - Severity unknown

**💡 Why this matters:** This is the MAIN hazard indicator - 41.2% are high-severity

---

### **3. ⚠️ MANDATORY_RPT**
**What it shows:** Legal reporting requirement code

- **30.0** (231 cases) - Specific mandatory reporting category
- **Empty** - Voluntary reports

**💡 Why this matters:** Shows which incidents triggered legal reporting requirements

---

### **4. 🏥 RISK_CLASSIFICATION**
**What it shows:** Medical device risk class (Health Canada classification)

- **Class 3** (264 cases) - High risk devices (life support, implants)
- **Class 2** (251 cases) - Medium risk devices  
- **Class 0** (43 cases) - Risk not assigned
- **Combined** (25 cases) - Multiple device classes involved

**💡 Why this matters:** Class 3 = highest risk medical devices

---

### **5. 📅 DATE COLUMNS**
**What they show:** Timeline of hazard events

- **INCIDENT_DT** - When the problem actually happened
- **INC_AWARE_DT** - When authorities became aware  
- **RECEIPT_DT** - When report was received

**💡 Why this matters:** Shows reporting delays and incident patterns

---

### **6. 🏢 COMPANY/ROLE COLUMNS**
**What they show:** Who was involved in the incident

- **COMPANY_NAME** - Device manufacturers, hospitals
- **ROLE_E** - (MANUFACTURER), (HOSPITAL), (IMPORTER)

**💡 Why this matters:** Identifies responsible parties

---

## 🔍 **EXAMPLE: How Hazard Info Looks**

```
INCIDENT_ID: 1113831
INCIDENT_TYPE_E: Mandatory problem report ← Required to report
HAZARD_SEVERITY_CODE_E: POTENTIAL FOR DEATH/INJURY ← HIGH RISK
MANDATORY_RPT: 30.0 ← Legal requirement triggered
RISK_CLASSIFICATION: 3 ← Highest risk device class
TRADE_NAME: SPACE INFUSION SYSTEM ← Problem device
```

---

## ⚠️ **WHAT'S MISSING (The Critical Gap)**

### **What Canadian Columns Tell Us:**
✅ **THAT** a hazard occurred  
✅ **HOW SEVERE** it was rated  
✅ **WHEN** it happened  
✅ **WHO** was involved  
✅ **WHAT DEVICE** was involved  

### **What Canadian Columns DON'T Tell Us:**
❌ **WHAT** actually went wrong  
❌ **HOW** the device failed  
❌ **WHY** it was dangerous  
❌ **WHAT** the patient experienced  
❌ **HOW** staff responded  

---

## 🎯 **Bottom Line**

The Canadian database has **good structural data** about device hazards:
- **41.2% high-severity incidents** (death/injury potential/actual injury)
- **40.6% mandatory reports** (legally required)
- **44.9% Class 3 devices** (highest risk category)

**But it lacks the EVENT NARRATIVES that would explain HOW these hazards actually occurred.**

**Result:** We can identify dangerous devices and severity patterns, but cannot extract specific evidence of device malfunctions like we can with FDA MAUDE data.