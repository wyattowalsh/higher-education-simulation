# Markdown Visualization Snippets

## For a rendition of Breslin's Model
```graph LR
   1[Customer]
   subgraph Organization
   subgraph Group A
   k[Negotiated Group Routine]
   end 
   subgraph Group B
   a[Ind1]
   b[Ind2]
   c[Ind3]
   d[Ind4]
   e[Personal Routine 1]
   f[Personal Routine 2]
   g[Personal Routine 3]
   h[Personal Routine 4]
   j[Negotiated Group Routine]
   end
   subgraph Group C
   n[Negotiated Group Routine]
   end
   i[Organizational Routine]
   z[Customer Offering]
   end

   1 -->|"1: Give Feedback f(t)"|a & b & c & d 
   1 -->|"1: Give Feedback f(t)"| k & n


   a -->|"2: Interpret Feedback f(t)_1"| a
   b -->|"2: Interpret Feedback f(t)_2"| b
   c -->|"2: Interpret Feedback f(t)_3"| c
   d -->|"2: Interpret  f(t)_4"| d

   a -->|"3: Change Opinion"| e
   b -->|"3: Change Opinion"| f
   c -->|"3: Change Opinion"| g
   d -->|"3: Change Opinion"| h

   e -->|"4: Negotiate Within Group"| j
   f -->|"4: Negotiate Within Group"|j
   g -->|"4: Negotiate Within Group"|j
   h -->|"4: Negotiate Within Group"|j

   j & k & n -->|"5: Negotiate Between Groups"| i

   i -->|"Generates Products or Services"| z
   z -->|"Given to Customer"|1

```
## HEI Model Overview
```
graph LR
   subgraph HEI
   org[Institutional Policies and Routines]
   subgraph Students
   stus[Group Routine]
   stu[Particular Ideal Routine]
   end 
   subgraph Faculty
  
   facs[Group Routine]
   fac[Particular Ideal Routine]
   end


   subgraph Administration
   admins[Group Routine]
   admin[Particular Ideal Routine]
   end
   subgraph "Other Stakeholders"
   stakes[Group Routine]
   stake[Particular Ideal Routine]
   end
   end
   ex_inf_stu[External Influences]
   ex_inf_fac[External Influences]
   ex_inf_admin[External Influences]
   ex_inf_other[External Influences]

   ex_inf_stu ---->stu
   ex_inf_fac ---->fac
   ex_inf_admin ----> admin
   ex_inf_other ----> stake

   stu ---->|"Negotiate Within Groups"| stus
   fac ---->|"Negotiate Within Groups"| facs
   admin ---->|"Negotiate Within Groups"| admins
   stake ---->|"Negotiate Within Groups"| stakes


   stus & facs & admins & stakes -->|"Negotiate Between Groups"| org

   org -------> stu & fac & admin & stake

```
   
