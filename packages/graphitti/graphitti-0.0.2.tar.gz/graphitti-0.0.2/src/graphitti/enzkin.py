import pandas as pd
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
from scipy import stats
from typing import Optional, Tuple, Dict, Union
from abc import ABC, abstractmethod

class EnzymeKineticsBase(ABC):
    """Base class for enzyme kinetics visualization."""
    
    def __init__(self):
        self.style_params = {
            'style': 'darkgrid',
            'context': 'notebook',
            'font_scale': 1.2,
            'palette': 'magma'
        }
    
    example_data = {
        'single': pd.DataFrame({
            '[S]': [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0],
            'v': [0.085, 0.15, 0.25, 0.31, 0.36, 0.40, 0.45, 0.48]
        }),
        'multi': pd.DataFrame({
            'Enzyme': ['Enzyme A'] * 8 + ['Enzyme B'] * 8,
            '[S]': [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0] * 2,
            'v': [0.085, 0.15, 0.25, 0.31, 0.36, 0.40, 0.45, 0.48,  # Enzyme A
                 0.065, 0.12, 0.20, 0.25, 0.29, 0.32, 0.36, 0.38]   # Enzyme B
        })
    }
    
    @staticmethod
    def mm_equation(S, Vmax, Km):
        """Michaelis-Menten equation for curve fitting."""
        return (Vmax * S) / (Km + S)
    
    @staticmethod
    def calculate_r2(y_true, y_pred):
        """Calculate R-squared value for goodness of fit."""
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot)

    def _format_plot(self, plot, title, xlabel, ylabel, params, figsize):
        """Format plot with labels, title, and parameter text box."""
        plot.set_title(title, fontsize=16, pad=15)
        plot.set_xlabel(xlabel, fontsize=14)
        plot.set_ylabel(ylabel, fontsize=14)
        
        text_params = []
        for name, p in params.items():
            if len(params) > 1:
                text_params.append(f'{name}:\n')
            text_params.append(
                f'Km = {p["Km"]:.2f} mM\n'
                f'Vmax = {p["Vmax"]:.2f} μmol/min\n'
                f'R² = {p["R²"]:.3f}\n'
            )
        
        plot.text(0.02, 0.98, '\n'.join(text_params),
                 transform=plot.transAxes,
                 fontsize=10, verticalalignment='top',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        plot.figure.set_size_inches(*figsize)
        plot.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plot.figure.set_constrained_layout(True)

    @abstractmethod
    def analyze(self, df, substrate_col, velocity_col, enzyme_col, figsize, title, style):
        """Abstract method to be implemented by derived classes."""
        pass


class MichaelisMenten(EnzymeKineticsBase):
    """Create publication-ready Michaelis-Menten plots using direct non-linear fitting."""
    
    def fit_enzyme_data(self, data_subset: pd.DataFrame, 
                       substrate_col: str, velocity_col: str) -> Tuple[float, float, float]:
        """Fit Michaelis-Menten equation to data subset."""
        v_max_guess = data_subset[velocity_col].max() * 1.2
        km_guess = data_subset[substrate_col].median()
        
        popt, _ = curve_fit(
            self.mm_equation,
            data_subset[substrate_col],
            data_subset[velocity_col],
            p0=[v_max_guess, km_guess],
            bounds=([0, 0], [np.inf, np.inf])
        )
        
        Vmax, Km = popt
        y_pred = self.mm_equation(data_subset[substrate_col], Vmax, Km)
        r_squared = self.calculate_r2(data_subset[velocity_col], y_pred)
        
        return Vmax, Km, r_squared

    def analyze(self,
               df: Optional[pd.DataFrame] = None,
               substrate_col: str = '[S]',
               velocity_col: str = 'v',
               enzyme_col: Optional[str] = None,
               figsize: Tuple[int, int] = (12, 8),
               title: str = 'Michaelis-Menten Plot',
               style: Optional[Dict] = None) -> Tuple[sns.FacetGrid, Dict[str, Dict[str, float]]]:
        """Create a Michaelis-Menten plot from enzyme kinetics data."""
        
        if df is None:
            df = self.example_data['multi' if enzyme_col else 'single']
        
        style_params = self.style_params.copy()
        if style:
            style_params.update(style)
        
        sns.set_style(style_params['style'])
        sns.set_context(style_params['context'], font_scale=style_params['font_scale'])
        
        plot = sns.scatterplot(
            data=df,
            x=substrate_col,
            y=velocity_col,
            hue=enzyme_col if enzyme_col else None,
            style=enzyme_col if enzyme_col else None,
            s=80
        )
        
        kinetic_params = {}
        S_range = np.linspace(0, df[substrate_col].max() * 1.1, 100)
        
        if enzyme_col:
            for enzyme in df[enzyme_col].unique():
                enzyme_data = df[df[enzyme_col] == enzyme]
                Vmax, Km, r_squared = self.fit_enzyme_data(
                    enzyme_data, substrate_col, velocity_col
                )
                kinetic_params[enzyme] = {
                    'Km': Km,
                    'Vmax': Vmax,
                    'R²': r_squared
                }
                v_fitted = self.mm_equation(S_range, Vmax, Km)
                plot.plot(S_range, v_fitted, label=f'{enzyme} Fit')
        else:
            Vmax, Km, r_squared = self.fit_enzyme_data(df, substrate_col, velocity_col)
            kinetic_params['enzyme'] = {
                'Km': Km,
                'Vmax': Vmax,
                'R²': r_squared
            }
            v_fitted = self.mm_equation(S_range, Vmax, Km)
            plot.plot(S_range, v_fitted, label='Fitted Curve')
        
        self._format_plot(plot, title, f'{substrate_col} (mM)',
                         f'{velocity_col} (μmol/min)', kinetic_params, figsize)
        
        return plot, kinetic_params


class Lineweaver(EnzymeKineticsBase):
    """Create publication-ready Lineweaver-Burk plots with intercept annotations."""
    
    def __init__(self):
        """Initialize with default style parameters."""
        self.style_params = {
            'style': 'ticks',
            'context': 'notebook',
            'font_scale': 1.2,
            'palette': 'bright'
        }

    def calculate_regression(self, data_subset: pd.DataFrame,
                           inv_substrate_col: str,
                           inv_velocity_col: str) -> Tuple[float, float, float, float, float]:
        """Calculate linear regression for Lineweaver-Burk plot."""
        x_data = data_subset[inv_substrate_col].values
        y_data = data_subset[inv_velocity_col].values
        
        sort_idx = np.argsort(x_data)
        x_data = x_data[sort_idx]
        y_data = y_data[sort_idx]
        
        slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
        
        Vmax = 1 / intercept
        Km = slope * Vmax
        x_intercept = -1/Km
        
        return Km, Vmax, r_value**2, intercept, x_intercept

    def _add_intercept_annotations(self, plot, x_intercept, y_intercept, color, index=0):
        """Add annotations for x and y intercepts with smart positioning to avoid overlap."""
        # Y-intercept annotation (1/Vmax)
        plot.annotate(
            f'1/Vmax = {y_intercept:.3f}',
            xy=(0, y_intercept),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8,
            color=color,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1),
            ha='left',
            va='bottom'
        )
        
        # X-intercept annotation (-1/Km)
        # Alternate near/above x-axis, with "below" position just under the dots
        y_offset = 5 if index % 2 == 0 else 15  # Changed from -20 to 5 for the lower position
        
        plot.annotate(
            f'-1/Km = {x_intercept:.3f}',
            xy=(x_intercept, 0),
            xytext=(0, y_offset),
            textcoords='offset points',
            fontsize=8,
            color=color,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1),
            ha='center',
            va='bottom'
        )

    def analyze(self,
               df: Optional[pd.DataFrame] = None,
               substrate_col: str = '[S]',
               velocity_col: str = 'v',
               enzyme_col: Optional[str] = None,
               figsize: Tuple[int, int] = (12, 8),
               title: str = 'Lineweaver-Burk Plot',
               style: Optional[Dict] = None) -> Tuple[sns.FacetGrid, Dict[str, Dict[str, float]]]:
        """Create a Lineweaver-Burk plot from enzyme kinetics data."""
        
        if df is None:
            if enzyme_col:
                df = self.example_data['multi'].copy()
            else:
                df = self.example_data['single'].copy()
        
        required_cols = [substrate_col, velocity_col]
        if enzyme_col:
            required_cols.append(enzyme_col)
            
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        if (df[substrate_col] <= 0).any() or (df[velocity_col] <= 0).any():
            raise ValueError("Substrate concentrations and velocities must be positive")
        
        style_params = self.style_params.copy()
        if style:
            style_params.update(style)
        
        sns.set_style(style_params['style'])
        sns.set_context(style_params['context'], font_scale=style_params['font_scale'])
        
        plot_df = pd.DataFrame()
        plot_df[substrate_col] = df[substrate_col]
        plot_df[velocity_col] = df[velocity_col]
        plot_df[f'1/{substrate_col}'] = 1 / df[substrate_col]
        plot_df[f'1/{velocity_col}'] = 1 / df[velocity_col]
        
        if enzyme_col:
            plot_df[enzyme_col] = df[enzyme_col]
            unique_enzymes = plot_df[enzyme_col].unique()
            n_colors = len(unique_enzymes)
            palette = sns.color_palette(style_params['palette'], n_colors=n_colors)
            color_mapping = dict(zip(unique_enzymes, palette))
        
        scatter = sns.scatterplot(
            data=plot_df,
            x=f'1/{substrate_col}',
            y=f'1/{velocity_col}',
            hue=enzyme_col if enzyme_col else None,
            style=enzyme_col if enzyme_col else None,
            palette=color_mapping if enzyme_col else None,
            s=80
        )
        
        kinetic_params = {}
        all_y_intercepts = []
        all_x_intercepts = []
        
        if enzyme_col:
            for idx, enzyme in enumerate(unique_enzymes):
                enzyme_data = plot_df[plot_df[enzyme_col] == enzyme].copy()
                enzyme_data = enzyme_data.sort_values(by=f'1/{substrate_col}')
                
                Km, Vmax, r_squared, y_intercept, x_intercept = self.calculate_regression(
                    enzyme_data, f'1/{substrate_col}', f'1/{velocity_col}'
                )
                
                all_y_intercepts.append(y_intercept)
                all_x_intercepts.append(x_intercept)
                
                kinetic_params[enzyme] = {
                    'Km': Km,
                    'Vmax': Vmax,
                    'R²': r_squared
                }
                
                data_x_max = plot_df[f'1/{substrate_col}'].max()
                data_x_min = plot_df[f'1/{substrate_col}'].min()
                plot_range = max(abs(x_intercept), data_x_max, abs(data_x_min)) * 1.2
                
                x_range = np.linspace(-plot_range, plot_range, 100)
                y_vals = x_range * (Km/Vmax) + 1/Vmax
                
                color = color_mapping[enzyme]
                scatter.plot(x_range, y_vals, 
                           color=color,
                           label=f'{enzyme} Regression')
                
                scatter.plot(0, y_intercept, 'o', color=color, markersize=6)
                scatter.plot(x_intercept, 0, 'o', color=color, markersize=6)
                
                self._add_intercept_annotations(scatter, x_intercept, y_intercept, color, idx)
        
        else:
            regression_df = plot_df[[f'1/{substrate_col}', f'1/{velocity_col}']].copy()
            Km, Vmax, r_squared, y_intercept, x_intercept = self.calculate_regression(
                regression_df, f'1/{substrate_col}', f'1/{velocity_col}'
            )
            all_y_intercepts.append(y_intercept)
            all_x_intercepts.append(x_intercept)
            
            data_x_max = plot_df[f'1/{substrate_col}'].max()
            plot_range = max(abs(x_intercept), data_x_max) * 1.2
            
            x_range = np.linspace(-plot_range, plot_range, 100)
            y_vals = x_range * (Km/Vmax) + 1/Vmax
            color = sns.color_palette()[0]
            scatter.plot(x_range, y_vals, color=color, label='Regression Line')
            
            kinetic_params['enzyme'] = {
                'Km': Km,
                'Vmax': Vmax,
                'R²': r_squared
            }
            
            scatter.plot(0, y_intercept, 'o', color=color, markersize=6)
            scatter.plot(x_intercept, 0, 'o', color=color, markersize=6)
            
            self._add_intercept_annotations(scatter, x_intercept, y_intercept, color)
        
        # Add axes lines
        scatter.axvline(x=0, linewidth=1.25, color='gray')
        scatter.axhline(y=0, linewidth=1.25, color='gray')
        
        # Calculate tighter bounds focused on intercepts
        y_intercept_max = max(all_y_intercepts)
        x_intercept_min = min(all_x_intercepts)
        
        # Set x-axis limits to show just enough of the negative region for -1/Km
        # and a bit of the positive region for data trend
        x_view_min = x_intercept_min * 1.2  # Give 20% padding for negative side
        x_view_max = -x_intercept_min * 0.8  # Show less of the positive side
        
        # Set y-axis limits to focus on 1/Vmax region
        # Show up to about 2.5x the highest y-intercept
        y_view_max = y_intercept_max * 2.5
        
        scatter.set_xlim(x_view_min, x_view_max)
        scatter.set_ylim(-0.1 * y_intercept_max, y_view_max)
        
        self._format_plot(scatter, title, f'1/{substrate_col} (mM⁻¹)',
                         f'1/{velocity_col} (min/μmol)', kinetic_params, figsize)
        
        return scatter, kinetic_params