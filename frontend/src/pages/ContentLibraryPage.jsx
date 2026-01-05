import ContentList from '../components/content/ContentList'

export default function ContentLibraryPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Content Library</h1>
      <ContentList />
    </div>
  )
}
