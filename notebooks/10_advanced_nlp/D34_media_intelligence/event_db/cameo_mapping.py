"""
CAMEO Event Code to Socioeconomic Domain Mapping

Maps GDELT CAMEO event codes to socioeconomic domains and categories.
Based on CAMEO (Conflict and Mediation Event Observations) taxonomy:
https://www.gdeltproject.org/data/documentation/CAMEO.Manual.1.1b3.pdf

Domains:
- labor_and_employment: Labor actions, union activity, worker rights
- health_and_social_policy: Healthcare, welfare, social safety nets
- inequality_and_poverty: Economic disparities, poverty, marginalization
- education_and_youth: Education policy, student protests, youth issues
- governance_and_corruption: Government actions, corruption, reforms
- climate_and_environment: Environmental disasters, climate policy

Author: KRL Team
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .config import get_cameo_codes_path

logger = logging.getLogger(__name__)


class CAMEOMapper:
    """Maps CAMEO event codes to socioeconomic domains."""
    
    # CAMEO event code ranges by quadrant
    # Quad 1: Verbal Cooperation (01-05)
    # Quad 2: Material Cooperation (06-08)
    # Quad 3: Verbal Conflict (09-15)
    # Quad 4: Material Conflict (16-20)
    
    # Core mapping: event_root_code -> (domain, category, confidence)
    CAMEO_MAPPING = {
        # Labor & Employment
        '14': ('labor_and_employment', 'labor_action', 0.95),  # Protest, demonstrate
        '145': ('labor_and_employment', 'labor_action', 1.0),  # Conduct strike or boycott
        '1451': ('labor_and_employment', 'labor_action', 1.0), # Conduct strike
        '06': ('labor_and_employment', 'policy_announcement', 0.80),  # Grant, cooperate economically
        '061': ('labor_and_employment', 'policy_announcement', 0.85), # Cooperate economically
        
        # Health & Social Policy
        '02': ('health_and_social_policy', 'humanitarian_aid', 0.75),  # Appeal, request
        '07': ('health_and_social_policy', 'humanitarian_aid', 0.90),  # Provide aid
        '071': ('health_and_social_policy', 'humanitarian_aid', 0.95), # Provide humanitarian aid
        '072': ('health_and_social_policy', 'healthcare_provision', 0.95), # Provide economic aid
        '087': ('health_and_social_policy', 'healthcare_provision', 0.90), # Grant asylum
        
        # Inequality & Poverty
        '12': ('inequality_and_poverty', 'discrimination', 0.85),  # Disapprove, reject
        '13': ('inequality_and_poverty', 'discrimination', 0.80),  # Reduce, yield
        '18': ('inequality_and_poverty', 'violence_against_civilians', 0.90),  # Assault
        '181': ('inequality_and_poverty', 'violence_against_civilians', 0.95), # Abduct, hijack
        '182': ('inequality_and_poverty', 'violence_against_civilians', 0.95), # Physically assault
        
        # Education & Youth
        '141': ('education_and_youth', 'student_protest', 0.90),  # Demonstrate, march
        '1411': ('education_and_youth', 'student_protest', 0.95), # Demonstrate
        '04': ('education_and_youth', 'policy_announcement', 0.70),  # Consult, negotiate
        
        # Governance & Corruption
        '10': ('governance_and_corruption', 'legal_action', 0.90),  # Demand, appeal formally
        '101': ('governance_and_corruption', 'legal_action', 0.95), # Demand compliance
        '11': ('governance_and_corruption', 'sanctions', 0.90),  # Disapprove, criticize
        '19': ('governance_and_corruption', 'military_action', 0.85),  # Fight, engage in violence
        '172': ('governance_and_corruption', 'sanctions', 0.90),  # Impose embargo, boycott
        
        # Climate & Environment
        '143': ('climate_and_environment', 'environmental_protest', 0.90),  # Protest environmental
        '20': ('climate_and_environment', 'environmental_disaster', 0.80),  # Engage in unconventional mass violence
    }
    
    # Domain keywords for fallback categorization
    DOMAIN_KEYWORDS = {
        'labor_and_employment': ['strike', 'labor', 'worker', 'union', 'wage', 'employment', 'job'],
        'health_and_social_policy': ['health', 'medical', 'hospital', 'aid', 'welfare', 'humanitarian'],
        'inequality_and_poverty': ['poverty', 'inequality', 'discriminat', 'marginalize', 'disparity'],
        'education_and_youth': ['student', 'education', 'school', 'university', 'youth', 'learn'],
        'governance_and_corruption': ['government', 'corrupt', 'sanction', 'legal', 'court', 'law'],
        'climate_and_environment': ['climate', 'environment', 'pollut', 'disaster', 'flood', 'drought']
    }
    
    def __init__(self, custom_mapping_path: Optional[Path] = None):
        """Initialize CAMEO mapper.
        
        Args:
            custom_mapping_path: Optional path to custom JSON mapping file
        """
        self.mapping = self.CAMEO_MAPPING.copy()
        
        # Load custom mappings if provided
        if custom_mapping_path and custom_mapping_path.exists():
            self._load_custom_mapping(custom_mapping_path)
    
    def _load_custom_mapping(self, path: Path):
        """Load custom CAMEO mapping from JSON file.
        
        Args:
            path: Path to JSON file with custom mappings
        """
        try:
            with open(path, 'r') as f:
                custom = json.load(f)
                self.mapping.update(custom)
                logger.info(f"Loaded {len(custom)} custom CAMEO mappings from {path}")
        except Exception as e:
            logger.error(f"Failed to load custom mapping: {e}")
    
    def categorize_event(self, event_code: str) -> Dict:
        """Categorize a GDELT event by its CAMEO code.
        
        Args:
            event_code: CAMEO event code (e.g., '1451', '071')
            
        Returns:
            Dict with 'domain', 'category', 'confidence' keys
        """
        if not event_code:
            return {
                'domain': 'uncategorized',
                'category': 'unknown',
                'confidence': 0.0
            }
        
        # Try exact match first (most specific)
        if event_code in self.mapping:
            domain, category, confidence = self.mapping[event_code]
            return {
                'domain': domain,
                'category': category,
                'confidence': confidence
            }
        
        # Try root code (first 2 digits)
        root_code = event_code[:2]
        if root_code in self.mapping:
            domain, category, confidence = self.mapping[root_code]
            return {
                'domain': domain,
                'category': category,
                'confidence': confidence * 0.8  # Lower confidence for broader match
            }
        
        # Try base code (first digit)
        base_code = event_code[:1]
        if base_code in self.mapping:
            domain, category, confidence = self.mapping[base_code]
            return {
                'domain': domain,
                'category': category,
                'confidence': confidence * 0.6  # Even lower confidence
            }
        
        # Default: uncategorized
        return {
            'domain': 'uncategorized',
            'category': 'unknown',
            'confidence': 0.0
        }
    
    def categorize_by_quad_class(self, quad_class: int) -> str:
        """Map quad class to general domain.
        
        Args:
            quad_class: CAMEO quad class (1-4)
            
        Returns:
            General domain string
        """
        quad_map = {
            1: 'cooperation_verbal',      # Verbal Cooperation
            2: 'cooperation_material',     # Material Cooperation
            3: 'conflict_verbal',          # Verbal Conflict
            4: 'conflict_material'         # Material Conflict
        }
        return quad_map.get(quad_class, 'unknown')
    
    def get_domain_distribution(self, event_codes: List[str]) -> Dict[str, int]:
        """Count events by socioeconomic domain.
        
        Args:
            event_codes: List of CAMEO event codes
            
        Returns:
            Dict mapping domain -> count
        """
        distribution = {}
        for code in event_codes:
            result = self.categorize_event(code)
            domain = result['domain']
            distribution[domain] = distribution.get(domain, 0) + 1
        return distribution
    
    def export_mapping(self, output_path: Path):
        """Export current mapping to JSON file.
        
        Args:
            output_path: Path to save JSON mapping
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(self.mapping, f, indent=2)
                logger.info(f"Exported CAMEO mapping to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export mapping: {e}")
    
    def add_custom_mapping(self, event_code: str, domain: str, category: str, confidence: float):
        """Add or update a custom CAMEO mapping.
        
        Args:
            event_code: CAMEO code to map
            domain: Socioeconomic domain
            category: Specific category
            confidence: Confidence score (0.0-1.0)
        """
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        self.mapping[event_code] = (domain, category, confidence)
        logger.info(f"Added mapping: {event_code} -> {domain}/{category} ({confidence})")


def main():
    """Example usage and testing."""
    logging.basicConfig(level=logging.INFO)
    
    mapper = CAMEOMapper()
    
    # Test common CAMEO codes
    test_codes = [
        ('1451', 'Labor strike'),
        ('071', 'Humanitarian aid'),
        ('18', 'Assault'),
        ('141', 'Demonstration'),
        ('10', 'Demand'),
        ('143', 'Environmental protest'),
        ('999', 'Unknown code')
    ]
    
    print("\n=== CAMEO Categorization Examples ===")
    for code, description in test_codes:
        result = mapper.categorize_event(code)
        print(f"{code} ({description}):")
        print(f"  Domain: {result['domain']}")
        print(f"  Category: {result['category']}")
        print(f"  Confidence: {result['confidence']:.2f}\n")
    
    # Test distribution
    codes = ['1451', '1451', '071', '18', '141', '10']
    distribution = mapper.get_domain_distribution(codes)
    print("=== Domain Distribution ===")
    for domain, count in sorted(distribution.items(), key=lambda x: -x[1]):
        print(f"{domain}: {count}")


if __name__ == '__main__':
    main()
