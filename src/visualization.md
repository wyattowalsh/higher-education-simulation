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
   
