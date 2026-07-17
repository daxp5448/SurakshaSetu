import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Renders bot replies (markdown) as structured, styled content
// instead of a single wall-of-text paragraph.
export default function ChatMarkdown({ text, size = 'sm' }) {
  const base = size === 'xs' ? 'text-xs' : 'text-sm';

  return (
    <div className={`${base} leading-relaxed space-y-2 [&_p]:my-0`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <h3 className="font-semibold text-primary mt-2">{children}</h3>,
          h2: ({ children }) => <h3 className="font-semibold text-primary mt-2">{children}</h3>,
          h3: ({ children }) => <h4 className="font-semibold text-primary mt-2">{children}</h4>,
          strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
          ul: ({ children }) => <ul className="list-disc pl-4 space-y-1.5 my-1">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal pl-4 space-y-1.5 my-1">{children}</ol>,
          li: ({ children }) => <li className="marker:text-primary">{children}</li>,
          a: ({ href, children }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary underline underline-offset-2">
              {children}
            </a>
          ),
          code: ({ inline, children }) =>
            inline ? (
              <code className="bg-white/10 rounded px-1 py-0.5 text-[0.85em]">{children}</code>
            ) : (
              <pre className="bg-white/10 rounded-lg p-2 overflow-x-auto my-1">
                <code>{children}</code>
              </pre>
            ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-primary/50 pl-3 text-muted-foreground my-1">
              {children}
            </blockquote>
          ),
          hr: () => <hr className="border-white/10 my-2" />,
        }}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
}
