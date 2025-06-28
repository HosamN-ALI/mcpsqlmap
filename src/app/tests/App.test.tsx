import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../app/page';

describe('App Component', () => {
  it('renders the main heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { name: /Advanced MCP SQLMap Server/i });
    expect(heading).toBeInTheDocument();
  });

  it('renders the scan button and responds to click', () => {
    render(<App />);
    const scanButton = screen.getByRole('button', { name: /Start Scan/i });
    expect(scanButton).toBeInTheDocument();
    fireEvent.click(scanButton);
    // Add assertions for expected behavior after click if applicable
  });

  it('renders payload list and allows searching', () => {
    render(<App />);
    const searchInput = screen.getByPlaceholderText(/Search payloads/i);
    expect(searchInput).toBeInTheDocument();
    fireEvent.change(searchInput, { target: { value: 'union' } });
    // Add assertions for filtered payload list if applicable
  });

  it('is responsive and accessible', () => {
    render(<App />);
    // Accessibility checks can be added here using axe or similar tools
    // For now, just check if main elements are present
    expect(screen.getByRole('main')).toBeInTheDocument();
  });
});
