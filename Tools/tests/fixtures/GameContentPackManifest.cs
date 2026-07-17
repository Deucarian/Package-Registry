namespace Deucarian.GameContentAuthoring
{
    internal sealed class GameContentPackSource
    {
        private bool required = true;

        public GameContentPackSource(bool isRequired = true)
        {
            required = isRequired;
        }

        public bool Required => required;
    }

    internal sealed class ModernRequiredMember
    {
        public required string Name { get; init; }
    }
}
