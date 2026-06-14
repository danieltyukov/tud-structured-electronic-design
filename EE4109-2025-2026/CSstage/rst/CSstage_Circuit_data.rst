

============
Circuit data
============




---------------
Circuit diagram
---------------




.. figure:: /img/CSstageSLiCAP.svg
    :width: 400




-------
Netlist
-------

.. literalinclude:: ../cir/CSstage.cir
    :linenos:




------------------------------
Expanded netlist  element data
------------------------------

.. csv-table::
    :delim: ;
    :header: RefDes, Nodes, Refs, Model, Param, Symbolic, Numeric
    :widths: 5 10 10 5 5 35 30
    
    R1;  out 0; ; R; value; :math:`R_{L}`; :math:`10000.0`
    Gm_M1_XU1;  out 0 N001 0; ; G; value; :math:`g_{\mathrm{m{XU1}}}`; :math:`0.001493`
    Gb_M1_XU1;  out 0 0 0; ; g; value; :math:`g_{\mathrm{b{XU1}}}`; :math:`0.0005226`
    Go_M1_XU1;  out 0 out 0; ; g; value; :math:`g_{\mathrm{o{XU1}}}`; :math:`5.0\cdot 10^{-6}`
    Cgs_M1_XU1;  N001 0; ; C; value; :math:`c_{\mathrm{{gs}{XU1}}}`; :math:`1.243\cdot 10^{-13}`
    Cgb_M1_XU1;  N001 0; ; C; value; :math:`c_{\mathrm{{gb}{XU1}}}`; :math:`1.456\cdot 10^{-14}`
    Cdg_M1_XU1;  out N001; ; C; value; :math:`c_{\mathrm{{dg}{XU1}}}`; :math:`1.2\cdot 10^{-14}`
    Csb_M1_XU1;  0 0; ; C; value; :math:`c_{\mathrm{{sb}{XU1}}}`; :math:`7.2\cdot 10^{-15}`
    Cdb_M1_XU1;  out 0; ; C; value; :math:`c_{\mathrm{{db}{XU1}}}`; :math:`7.2\cdot 10^{-15}`
    I1;  0 N001; ; I; value; :math:`0`; :math:`0.0`
     ; ; ; ;dc; :math:`0`; :math:`0.0`
     ; ; ; ;dcvar; :math:`0`; :math:`0.0`
     ; ; ; ;noise; :math:`0`; :math:`0.0`
    R2;  N001 0; ; R; value; :math:`R_{s}`; :math:`1.0\cdot 10^{+7}`




----------------------------
List with circuit parameters
----------------------------

.. csv-table::
    :header: name, symbolic, value
    :delim: ;
    :widths: 10 50 40

    :math:`W` ; :math:`4.0\cdot 10^{-5}` ; :math:`4.0\cdot 10^{-5}`
    :math:`L` ; :math:`5.0\cdot 10^{-7}` ; :math:`5.0\cdot 10^{-7}`
    :math:`\mathrm{ID}` ; :math:`0.0001` ; :math:`0.0001`
    :math:`R_{L}` ; :math:`10000.0` ; :math:`10000.0`
    :math:`R_{s}` ; :math:`1.0\cdot 10^{+7}` ; :math:`1.0\cdot 10^{+7}`
    :math:`E_{\mathrm{{CRIT}{XU1}}}` ; :math:`5.6\cdot 10^{+6}` ; :math:`5.6\cdot 10^{+6}`
    :math:`\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}` ; :math:`\frac{0.0625\,L^2\,{E_{\mathrm{{CRIT}{XU1}}}}^2}{{U_{T}}^2\,{N_{\mathrm{s{XU1}}}}^2\,{\left(L\,\mathrm{\Theta}_{\mathrm{XU1}}\,E_{\mathrm{{CRIT}{XU1}}}+1.0\right)}^2}` ; :math:`126.4`
    :math:`N_{\mathrm{s{XU1}}}` ; :math:`1.35` ; :math:`1.35`
    :math:`\mathrm{\Theta}_{\mathrm{XU1}}` ; :math:`0.28` ; :math:`0.28`
    :math:`U_{T}` ; :math:`\frac{T\,k}{q}` ; :math:`0.02585`
    :math:`\mathrm{IC}_{\mathrm{XU1}}` ; :math:`\frac{\mathrm{ID}\,L}{W\,I_{\mathrm{0{XU1}}}}` ; :math:`1.949`
    :math:`g_{\mathrm{m{XU1}}}` ; :math:`\frac{1.414\,\mathrm{ID}}{U_{T}\,N_{\mathrm{s{XU1}}}\,\sqrt{\frac{2.0\,\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}+\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}\,\sqrt{\frac{\mathrm{IC}_{\mathrm{XU1}}\,\left(\mathrm{IC}_{\mathrm{XU1}}+\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}\right)}{\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}}}+2.0\,\mathrm{IC}_{\mathrm{XU1}}\,\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}+2.0\,{\mathrm{IC}_{\mathrm{XU1}}}^2}{\mathrm{IC}_{\mathrm{{CRIT}{XU1}}}}}}` ; :math:`0.001493`
    :math:`\mathrm{VAL}_{\mathrm{XU1}}` ; :math:`4.0\cdot 10^{+7}` ; :math:`4.0\cdot 10^{+7}`
    :math:`g_{\mathrm{o{XU1}}}` ; :math:`\frac{\mathrm{ID}}{L\,\mathrm{VAL}_{\mathrm{XU1}}}` ; :math:`5.0\cdot 10^{-6}`
    :math:`g_{\mathrm{b{XU1}}}` ; :math:`g_{\mathrm{m{XU1}}}\,\left(N_{\mathrm{s{XU1}}}-1.0\right)` ; :math:`0.0005226`
    :math:`\mathrm{CGSO}_{\mathrm{XU1}}` ; :math:`3.0\cdot 10^{-10}` ; :math:`3.0\cdot 10^{-10}`
    :math:`C_{\mathrm{{OX}{XU1}}}` ; :math:`\frac{\mathrm{\epsilon}_{0}\,\mathrm{\epsilon}_{\mathrm{SiO2}}}{\mathrm{TOX}_{\mathrm{XU1}}}` ; :math:`0.008422`
    :math:`c_{\mathrm{{gs}{XU1}}}` ; :math:`0.3333\,W\,\left(3.0\,\mathrm{CGSO}_{\mathrm{XU1}}+2.0\,L\,C_{\mathrm{{OX}{XU1}}}\right)` ; :math:`1.243\cdot 10^{-13}`
    :math:`c_{\mathrm{{dg}{XU1}}}` ; :math:`W\,\mathrm{CGSO}_{\mathrm{XU1}}` ; :math:`1.2\cdot 10^{-14}`
    :math:`\mathrm{CGBO}_{\mathrm{XU1}}` ; :math:`1.0\cdot 10^{-12}` ; :math:`1.0\cdot 10^{-12}`
    :math:`c_{\mathrm{{gb}{XU1}}}` ; :math:`2.0\,L\,\mathrm{CGBO}_{\mathrm{XU1}}+\frac{0.3333\,L\,W\,C_{\mathrm{{OX}{XU1}}}\,\left(N_{\mathrm{s{XU1}}}-1.0\right)}{N_{\mathrm{s{XU1}}}}` ; :math:`1.456\cdot 10^{-14}`
    :math:`\mathrm{CJB0}_{\mathrm{XU1}}` ; :math:`0.001` ; :math:`0.001`
    :math:`\mathrm{LDS}_{\mathrm{XU1}}` ; :math:`1.8\cdot 10^{-7}` ; :math:`1.8\cdot 10^{-7}`
    :math:`c_{\mathrm{{db}{XU1}}}` ; :math:`W\,\mathrm{CJB0}_{\mathrm{XU1}}\,\mathrm{LDS}_{\mathrm{XU1}}` ; :math:`7.2\cdot 10^{-15}`
    :math:`c_{\mathrm{{sb}{XU1}}}` ; :math:`W\,\mathrm{CJB0}_{\mathrm{XU1}}\,\mathrm{LDS}_{\mathrm{XU1}}` ; :math:`7.2\cdot 10^{-15}`
    :math:`I_{\mathrm{0{XU1}}}` ; :math:`2.0\,{U_{T}}^2\,C_{\mathrm{{OX}{XU1}}}\,N_{\mathrm{s{XU1}}}\,u_{\mathrm{0{XU1}}}` ; :math:`6.413\cdot 10^{-7}`
    :math:`u_{\mathrm{0{XU1}}}` ; :math:`0.0422` ; :math:`0.0422`
    :math:`\mathrm{TOX}_{\mathrm{XU1}}` ; :math:`4.1\cdot 10^{-9}` ; :math:`4.1\cdot 10^{-9}`
    :math:`\mathrm{\epsilon}_{0}` ; :math:`\frac{1}{c^2\,\mathrm{\mu}_{0}}` ; :math:`8.854\cdot 10^{-12}`
    :math:`\mathrm{\epsilon}_{\mathrm{SiO2}}` ; :math:`3.9` ; :math:`3.9`
    :math:`V_{\mathrm{{GS}{XU1}}}` ; :math:`\mathrm{Vth}_{\mathrm{XU1}}+2.0\,U_{T}\,N_{\mathrm{s{XU1}}}\,\ln\left({\mathrm{e}}^{\sqrt{\mathrm{IC}_{\mathrm{XU1}}}}-1.0\right)` ; :math:`0.4376`
    :math:`\mathrm{Vth}_{\mathrm{XU1}}` ; :math:`0.36` ; :math:`0.36`
    :math:`c_{\mathrm{{iss}{XU1}}}` ; :math:`c_{\mathrm{{gb}{XU1}}}+c_{\mathrm{{dg}{XU1}}}+c_{\mathrm{{gs}{XU1}}}` ; :math:`1.509\cdot 10^{-13}`
    :math:`f_{\mathrm{T{XU1}}}` ; :math:`\frac{0.1592\,g_{\mathrm{m{XU1}}}}{c_{\mathrm{{iss}{XU1}}}}` ; :math:`1.575\cdot 10^{+9}`
    :math:`\pi ` ; :math:`3.142` ; :math:`3.142`


