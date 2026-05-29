import { SSEInterceptor } from "../src/Renderer/Repository/SSEInterceptor";

describe("SSEInterceptor", () => {
  let interceptor: SSEInterceptor;
  let mockEventSource: EventSource;

  beforeEach(() => {
    // Mock EventSource
    mockEventSource = {
      onmessage: null,
      onerror: null,
      close: jest.fn(),
    } as unknown as EventSource;

    // Spy on EventSource constructor
    jest.spyOn(window, "EventSource").mockImplementation(() => mockEventSource);

    // Create interceptor instance
    interceptor = new SSEInterceptor("http://example.com/sse");
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("should modify and emit intercepted events", (done) => {
    const mockHandler = jest.fn();
    interceptor.on("message", mockHandler);

    // Simulate an SSE event
    const mockEvent = new MessageEvent("message", {
      data: JSON.stringify({ key: "value" }),
    });

    mockEventSource.onmessage(mockEvent);

    setTimeout(() => {
      expect(mockHandler).toHaveBeenCalledWith(
        expect.objectContaining({
          data: JSON.stringify({ key: "value", modified: true }),
        })
      );
      done();
    }, 0);
  });

  it("should handle errors and emit error events", (done) => {
    const mockErrorHandler = jest.fn();
    interceptor.on("error", mockErrorHandler);

    // Simulate an SSE error
    const mockError = new ErrorEvent("error", { message: "Test error" });
    mockEventSource.onerror(mockError);

    setTimeout(() => {
      expect(mockErrorHandler).toHaveBeenCalledWith(mockError);
      done();
    }, 0);
  });

  it("should stop listening to events when stopped", () => {
    interceptor.stop();
    expect(mockEventSource.close).toHaveBeenCalled();
  });
});