"use client"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

export default function TestReport() {
  const coverageData = [
    { component: "Core MCP Server", total: 12, passed: 11, failed: 1, coverage: 98 },
    { component: "Injection Techniques", total: 15, passed: 12, failed: 3, coverage: 74 },
    { component: "WAF Bypass Module", total: 20, passed: 15, failed: 5, coverage: 85 },
    { component: "Payload Manager", total: 20, passed: 12, failed: 8, coverage: 90 },
    { component: "Integration Manager", total: 15, passed: 5, failed: 10, coverage: 44 },
    { component: "API Routes", total: 0, passed: 0, failed: 0, coverage: 0 },
    { component: "Main Application", total: 0, passed: 0, failed: 0, coverage: 0 },
  ]

  return (
    <main className="container mx-auto py-10 px-4 space-y-10 max-w-7xl min-h-screen bg-background">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold tracking-tight mb-2">MCP Server Project - Test Report</h1>
            <p className="text-lg text-muted-foreground">
              Comprehensive test coverage and results summary for the advanced MCP server project
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-sm">Version 1.0</Badge>
            <Badge variant="secondary" className="text-sm">Test Suite</Badge>
          </div>
        </div>
        <div className="h-px bg-border" />
      </div>

      <Card className="shadow-md">
        <CardHeader>
          <CardTitle>Overview</CardTitle>
          <CardDescription>Project components and their testing status</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="list-disc pl-6 space-y-2">
            <li>Core MCP server with SQLMap integration</li>
            <li>Injection techniques module</li>
            <li>WAF bypass module</li>
            <li>Payload management system</li>
            <li>Integration manager with Deepseek API and Open WebUI</li>
            <li>API routes and main application entry point</li>
            <li>Comprehensive test suite covering unit and integration tests</li>
          </ul>
        </CardContent>
      </Card>

      <Card className="shadow-md">
        <CardHeader>
          <CardTitle>Test Coverage Summary</CardTitle>
          <CardDescription>Detailed breakdown of test results by component</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border shadow-sm">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Component</TableHead>
                  <TableHead className="text-right">Total Tests</TableHead>
                  <TableHead className="text-right">Passed</TableHead>
                  <TableHead className="text-right">Failed</TableHead>
                  <TableHead className="text-right">Coverage %</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {coverageData.map((row) => (
                  <TableRow key={row.component}>
                    <TableCell>{row.component}</TableCell>
                    <TableCell className="text-right">{row.total}</TableCell>
                    <TableCell className="text-right">
                      <span className="text-green-600 font-medium">{row.passed}</span>
                    </TableCell>
                    <TableCell className="text-right">
                      <span className="text-red-600 font-medium">{row.failed}</span>
                    </TableCell>
                    <TableCell className="text-right">
                      <Badge variant={row.coverage >= 75 ? "secondary" : row.coverage >= 50 ? "outline" : "destructive"}>
                        {row.coverage}%
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <Accordion type="single" collapsible className="space-y-4">
        <AccordionItem value="successful-tests" className="border rounded-lg px-6">
          <AccordionTrigger className="hover:no-underline">
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-sm">Passed</Badge>
              <h3 className="text-xl font-semibold">Successful Tests</h3>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <Card>
              <CardContent className="pt-6">
                <ul className="list-disc pl-6 space-y-2">
                  <li>Core MCP server initialization and SQLMap command execution.</li>
                  <li>Basic injection techniques: blind, union, stacked, stored procedure, out-of-band, NoSQL.</li>
                  <li>WAF bypass techniques: multiple individual techniques and combined tampering.</li>
                  <li>Payload manager: adding custom payloads, retrieving payloads by source and category.</li>
                  <li>Integration manager: initialization and basic Deepseek API communication (mocked).</li>
                  <li>API routes: basic endpoint functionality (manual testing recommended).</li>
                </ul>
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="failed-tests" className="border rounded-lg px-6">
          <AccordionTrigger className="hover:no-underline">
            <div className="flex items-center gap-2">
              <Badge variant="destructive" className="text-sm">Failed</Badge>
              <h3 className="text-xl font-semibold">Failed Tests and Issues</h3>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <div className="space-y-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle>Injection Techniques</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>Handling invalid injection technique did not raise expected exceptions.</li>
                    <li>Deepseek analysis method missing in InjectionHandler.</li>
                    <li>Error handling test expecting failure but success returned.</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Integration Manager</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>Async fixture usage issues causing test failures.</li>
                    <li>Attribute errors due to coroutine objects not awaited.</li>
                    <li>Missing or incorrect method implementations in tests.</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Payload Manager</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>Tests calling non-existent private methods (_load_fuzzdb_payloads, _load_pat_payloads, _load_nosql_payloads).</li>
                    <li>Search payloads test failed due to incorrect assertions.</li>
                    <li>Persistence test failed due to unexpected payload count.</li>
                    <li>Deepseek analysis method missing in PayloadManager.</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>WAF Bypass Module</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>Tests calling non-existent public methods (apply_whitespace_bypass etc.) instead of private methods.</li>
                    <li>Deepseek analysis test incorrectly using pytest fixture as context manager.</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>API Routes and Main Application</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>No automated tests implemented yet; manual testing recommended.</li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>External Payload Sources</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 space-y-2">
                    <li>Multiple 404 errors when loading payloads from GitHub raw URLs indicating outdated or moved resources.</li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="recommendations" className="border rounded-lg px-6">
          <AccordionTrigger className="hover:no-underline">
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-sm">Info</Badge>
              <h3 className="text-xl font-semibold">Recommendations</h3>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <Card>
              <CardContent className="pt-6">
                <ul className="list-disc pl-6 space-y-2">
                  <li>Fix test implementations to match current method names and async usage.</li>
                  <li>Implement API route tests using HTTP client libraries (e.g., httpx).</li>
                  <li>Add end-to-end tests simulating real SQLMap scans and Deepseek API responses.</li>
                  <li>Update payload source URLs or provide local payload files to avoid 404 errors.</li>
                  <li>Add security and authentication tests if applicable.</li>
                  <li>Increase test coverage for main.py and API routes.</li>
                  <li>Address warnings related to async fixtures and pytest-asyncio usage.</li>
                </ul>
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="conclusion" className="border rounded-lg px-6">
          <AccordionTrigger className="hover:no-underline">
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-sm">Summary</Badge>
              <h3 className="text-xl font-semibold">Conclusion</h3>
            </div>
          </AccordionTrigger>
          <AccordionContent>
            <Card>
              <CardContent className="pt-6">
                <p className="text-muted-foreground">
                  The project has a solid foundation with many core components tested successfully. Some tests require fixes due to code changes and async handling. External resource availability affects payload loading tests. With the recommended fixes and additional tests, the project will achieve robust test coverage and reliability.
                </p>
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </main>
  )
}
