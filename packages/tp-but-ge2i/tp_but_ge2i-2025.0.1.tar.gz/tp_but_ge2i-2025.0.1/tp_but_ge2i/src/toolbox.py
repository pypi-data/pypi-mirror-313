import pandapower as ppw
import pandas as pd
import numpy as np
from plotly.graph_objs.scattermapbox import Line
from pandapower.plotting.plotly.traces import create_bus_trace, create_line_trace, create_trafo_trace, draw_traces

def appliquer_coeffs(net : ppw.pandapowerNet, coeff_charge : float = 0, coeff_prod : float = 0):
    """
    Applique des coefficients relatifs aux charges et aux productions d'un réseau donné 
    
    INPUT:
        **net** (PandapowerNet) - réseau auquel appliquer les coefficients
        **coeff_charge** (float) - coefficient de charge à appliquer. 0 par défaut
        **coeff_prod** (float) - coefficient de production à appliquer. 0 par défaut
    """
    for indl in net.load.index:
        net.load.at[indl, "p_mw"] = net.load.at[indl, "max_p_mw"] * coeff_charge
    
    for inds in net.sgen.index:
        net.sgen.at[inds, 'p_mw'] = net.sgen.at[inds, 'max_p_mw'] * coeff_prod

def afficher_tensions(net : ppw.pandapowerNet):
    """
    Construit une figure plotly qui affiche les résultats du power flow pour un réseau HTA
    
    INPUT:
        **net** (pandapowerNet) - Le réseau à afficher. ATTENTION les tables de résultats doivent être complétés
    
    OUTPUT:
        **fig** (graph_objs._figure.Figure) - la figure plotly, prête à être affichée
    """
    buses = []
    bus_vals = []
    names = []
    trafos = []
    for ind_tr in net.trafo.index:
        if "T" in net.trafo.at[ind_tr, "name"]:
            trafos.append(ind_tr)
        else:
            buses.append(net.trafo.at[ind_tr, 'hv_bus'])
            bus_vals.append(net.res_bus.at[net.trafo.at[ind_tr, 'hv_bus'], "vm_pu"])
            names.append(net.trafo.at[ind_tr, 'name'])
   
    for ind_gen in net.sgen.index:
        if net.sgen.at[ind_gen, 'V_level'] == "HTA":
            buses.append(net.sgen.at[ind_gen, 'bus'])
            bus_vals.append(net.res_bus.at[net.sgen.at[ind_gen, 'bus'], "vm_pu"])
            names.append(net.sgen.at[ind_gen, 'name'])
    
    bus_self = []
    for ind_l in net.load.index:
        bus = net.load.at[ind_l, "bus"]
        if "Self" in net.load.at[ind_l, "name"]: 
            bus_self.append(bus)
        elif net.bus.at[bus, "vn_kv"] >= 20:
            buses.append(bus)
            bus_vals.append(net.res_bus.at[bus, "vm_pu"])
            names.append(f"Client {net.load.at[ind_l, 'name'].split('_')[-1]}")
    
    names = pd.Series(index = buses, data = names, dtype = "string", name = "name")
    
    hoverinfo = pd.Series(index = names.index, dtype = "string")
    for bus in hoverinfo.index:
        hoverinfo.at[bus] = f"{names.at[bus]}<br /> V_m (pu) : {net.res_bus.at[bus, 'vm_pu'].round(3)}<br /> V_m (kV) : {(net.res_bus.at[bus, 'vm_pu'] * net.bus.at[bus, 'vn_kv']).round(2)}<br /> V_a (°) : {net.res_bus.at[bus, 'va_degree'].round(3)}"

    line_info = pd.Series(index = net.line.index, dtype = "string")
    for line in line_info.index:
        line_info.at[line] = f"{net.line.at[line, "std_type"]} <br /> I : {net.res_line.at[line, 'i_ka'].round(4) * 1000} A <br /> Charge : {net.res_line.at[line, 'loading_percent'].round(1)} %"
    line_traces = create_line_trace(net, infofunc = line_info, cmap = "jet", cmap_vals = net.res_line["loading_percent"].values, show_colorbar = True, cbar_title = "charge des lignes", cmin = 0, cmax = 100, cpos = 1.1)
        
    x_jdb = []
    y_jdb = []
    bus_closed_switches = []
    info_closed_switches = []
    bus_open_switches = []
    info_open_switches = []
    for ind_sw in net.switch.index:
        if net.switch.at[ind_sw,'et'] == 'b':
            b1 = net.switch.at[ind_sw, 'bus']
            b2 = net.switch.at[ind_sw, 'element']
            x_jdb = x_jdb + [net.bus_geodata.at[b1, 'x'], net.bus_geodata.at[b2, 'x'], None]
            y_jdb = y_jdb + [net.bus_geodata.at[b1, 'y'], net.bus_geodata.at[b2, 'y'], None]
        if net.switch.at[ind_sw, 'name'] != 'jdb':
            if net.switch.at[ind_sw, 'closed']:
                if not net.switch.at[ind_sw, 'bus'] in bus_closed_switches:
                    bus_closed_switches.append(net.switch.at[ind_sw, 'bus'])
                    info_closed_switches.append(net.switch.at[ind_sw, 'name'])
            else:
                if not net.switch.at[ind_sw, 'bus'] in bus_open_switches:
                    bus_open_switches.append(net.switch.at[ind_sw, 'bus'])
                    info_open_switches.append(net.switch.at[ind_sw, 'name'])
    
    info_closed_switches = pd.Series(index = bus_closed_switches, data = info_closed_switches, dtype = "string")
    info_open_switches = pd.Series(index = bus_open_switches, data = info_open_switches, dtype = "string")
    info_ext_grid = pd.Series(index = net.ext_grid["bus"], dtype = "string")
    for ext_grid in net.ext_grid.index:
        info_ext_grid.at[net.ext_grid.at[ext_grid, "bus"]] = f"{net.ext_grid.at[ext_grid, "name"]} <br /> P : {net.res_ext_grid.at[ext_grid, "p_mw"].round(3)} MW <br /> Q : {net.res_ext_grid.at[ext_grid, "q_mvar"].round(3)} MVAr"
    
    
    bus_trace = create_bus_trace(net, hoverinfo.index.tolist(), 
                                 cmap = 'jet', 
                                 cmap_vals = bus_vals, 
                                 cbar_title = "tension aux noeuds",
                                 cmin = 0.9, 
                                 cmax = 1.1, 
                                 size = 8, 
                                 trace_name = "bus_trace", 
                                 infofunc = hoverinfo)
    
    jdb_trace = [dict(type = 'scatter', text = [], hoverinfo = 'none', mode = 'lines', name = 'jdb_trace',
                    line = Line(width = 2, color = 'grey'), x = x_jdb, y = y_jdb, connectgaps = False)]
    ext_grid_trace = create_bus_trace(net, net.ext_grid['bus'], color = 'grey', size = 12, trace_name = 'external_grid_trace', infofunc = info_ext_grid)
    
    closed_switches_trace = create_bus_trace(net, bus_closed_switches, patch_type = 'circle', size = 8, 
                                             color = "grey", trace_name = 'closed_switches_trace', infofunc = info_closed_switches)
    open_switches_trace = create_bus_trace(net, bus_open_switches, patch_type = 'circle', size = 8, 
                                           color = "purple", trace_name = 'open_switches_trace', infofunc = info_open_switches)
    
    if len(bus_self) > 0: 
        self_cmap = [(0., "hotpink"), (0.33, "hotpink"), (0.33, "magenta"), (0.66, "magenta"), (0.66, "violet"), (1., "violet")]
        self_trace = create_bus_trace(net, bus_self, patch_type = 'circle', size = 12, cmap = self_cmap, cmap_vals = np.linspace(0.9, 1.1, num = len(bus_self), dtype = float), cmin = 0.9, cmax = 1.1, cpos = 1, trace_name = "self_trace")
    else:
        self_trace = []
        
    trafo_trace = create_trafo_trace(net, trafos)
    
    fig = draw_traces(line_traces + jdb_trace + trafo_trace + closed_switches_trace + open_switches_trace + self_trace + ext_grid_trace + bus_trace, 
                      on_map = True, map_style = 'light', showlegend = False, aspect_ratio = (1., 1.))
    
    #return fig

def afficher_lignes_modifiables(net : ppw.pandapowerNet):
    """
    Construit une figure plotly qui met en évidence les lignes avec le plus de hausses de tensions
    
    INPUT:
        **net** (pandapowerNet) - Le réseau à afficher. ATTENTION les tables de résultats doivent être complétés
    
    OUTPUT:
        **fig** (graph_objs._figure.Figure) - la figure plotly, prête à être affichée
    """
    
    temp = {line : abs(net.res_bus.at[net.line.at[line, "to_bus"], "vm_pu"] - net.res_bus.at[net.line.at[line, "from_bus"], "vm_pu"]) for line in net.line.index}
    sorted_keys = sorted(temp, key = temp.get)
    delta_U = {key : temp[key] for key in sorted_keys}

    lines1 = list(delta_U.keys())[:-5]
    lines2 = list(delta_U.keys())[-5:]
    lines1.sort()
    lines2.sort()

    line_info1 = pd.Series(index = lines1, dtype = "string")
    for line in line_info1.index:
        line_info1.at[line] = f"Index : {line} <br /> {net.line.at[line, "std_type"]} <br /> I : {net.res_line.at[line, 'i_ka'].round(4) * 1000} A <br /> Charge : {net.res_line.at[line, 'loading_percent'].round(1)} % <br /> \u0394U : {(delta_U[line] * 100).round(1)} %"

    line_info2 = pd.Series(index = lines2, dtype = "string")
    for line in line_info2.index:
        line_info2.at[line] = f"Index : {line} <br /> {net.line.at[line, "std_type"]} <br /> I : {net.res_line.at[line, 'i_ka'].round(4) * 1000} A <br /> Charge : {net.res_line.at[line, 'loading_percent'].round(1)} % <br /> \u0394U : {(delta_U[line] * 100).round(1)} %"
    
    line_traces1 = create_line_trace(net, lines = lines1,
                                    infofunc = line_info1, cmap = "jet", cmap_vals = [net.res_line.at[line, "loading_percent"] for line in lines1], show_colorbar = True, 
                                    cbar_title = "charge des lignes", cmin = 0, cmax = 100, cpos = 1.1)

    line_traces2 = create_line_trace(net, lines = lines2, width = 4,
                                    infofunc = line_info2, cmap = "jet", cmap_vals = [net.res_line.at[line, "loading_percent"] for line in lines2], show_colorbar = True, 
                                    cbar_title = "charge des lignes", cmin = 0, cmax = 100, cpos = 1.1)
        
    x_jdb = []
    y_jdb = []
    bus_closed_switches = []
    info_closed_switches = []
    bus_open_switches = []
    info_open_switches = []
    for ind_sw in net.switch.index:
        if net.switch.at[ind_sw,'et'] == 'b':
            b1 = net.switch.at[ind_sw, 'bus']
            b2 = net.switch.at[ind_sw, 'element']
            x_jdb = x_jdb + [net.bus_geodata.at[b1, 'x'], net.bus_geodata.at[b2, 'x'], None]
            y_jdb = y_jdb + [net.bus_geodata.at[b1, 'y'], net.bus_geodata.at[b2, 'y'], None]
        if net.switch.at[ind_sw, 'name'] != 'jdb':
            if net.switch.at[ind_sw, 'closed']:
                if not net.switch.at[ind_sw, 'bus'] in bus_closed_switches:
                    bus_closed_switches.append(net.switch.at[ind_sw, 'bus'])
                    info_closed_switches.append(net.switch.at[ind_sw, 'name'])
            else:
                if not net.switch.at[ind_sw, 'bus'] in bus_open_switches:
                    bus_open_switches.append(net.switch.at[ind_sw, 'bus'])
                    info_open_switches.append(net.switch.at[ind_sw, 'name'])
    
    info_closed_switches = pd.Series(index = bus_closed_switches, data = info_closed_switches, dtype = "string")
    info_open_switches = pd.Series(index = bus_open_switches, data = info_open_switches, dtype = "string")
    info_ext_grid = pd.Series(index = net.ext_grid["bus"], dtype = "string")
    for ext_grid in net.ext_grid.index:
        info_ext_grid.at[net.ext_grid.at[ext_grid, "bus"]] = f"{net.ext_grid.at[ext_grid, "name"]} <br /> P : {net.res_ext_grid.at[ext_grid, "p_mw"].round(3)} MW <br /> Q : {net.res_ext_grid.at[ext_grid, "q_mvar"].round(3)} MVAr"
    
    jdb_trace = [dict(type = 'scatter', text = [], hoverinfo = 'none', mode = 'lines', name = 'jdb_trace',
                    line = Line(width = 2, color = 'grey'), x = x_jdb, y = y_jdb, connectgaps = False)]
    ext_grid_trace = create_bus_trace(net, net.ext_grid['bus'], color = 'grey', size = 12, trace_name = 'external_grid_trace', infofunc = info_ext_grid)
    
    closed_switches_trace = create_bus_trace(net, bus_closed_switches, patch_type = 'circle', size = 8, 
                                             color = "grey", trace_name = 'closed_switches_trace', infofunc = info_closed_switches)
    open_switches_trace = create_bus_trace(net, bus_open_switches, patch_type = 'circle', size = 8, 
                                           color = "purple", trace_name = 'open_switches_trace', infofunc = info_open_switches)
    
    
    fig = draw_traces(line_traces1 + line_traces2 + jdb_trace + closed_switches_trace + open_switches_trace + ext_grid_trace, 
                      on_map = True, map_style = 'light', showlegend = False, aspect_ratio = (1., 1.))




