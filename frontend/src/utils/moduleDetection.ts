export type ModuleType = 'afaqy' | 'order';

// Keywords and patterns that indicate Order-related queries
const ORDER_KEYWORDS = [
  'order',
  'purchase',
  'invoice',
  'delivery',
  'shipment',
  'tracking',
  'package',
  'shipping',
  'delivery date',
  'order status',
  'order number',
  'PO',
];

// Keywords and patterns that indicate Afaqy-related queries
const AFAQY_KEYWORDS = [
  'truck',
  'vehicle',
  'driver',
  'route',
  'location',
  'fleet',
  'maintenance',
  'schedule',
  'GPS',
  'tracking',
];

export function detectModuleType(query: string): ModuleType {
  const normalizedQuery = query.toLowerCase();
  
  // Count matches for each module
  const orderMatches = ORDER_KEYWORDS.filter(keyword => 
    normalizedQuery.includes(keyword.toLowerCase())
  ).length;
  
  const afaqyMatches = AFAQY_KEYWORDS.filter(keyword => 
    normalizedQuery.includes(keyword.toLowerCase())
  ).length;
  
  // Return the module with more keyword matches
  // Default to Afaqy if equal or no matches
  return orderMatches > afaqyMatches ? 'order' : 'afaqy';
} 